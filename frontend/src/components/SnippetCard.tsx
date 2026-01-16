import Snippet from "@/model/Snippet";
import { ComponentProps, useEffect, useState } from "react";
import Gravatar from "./Gravatar";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import BaseCodeMirror from "./BaseCodeMirror";
import { Button } from "./ui/button";
import { LucideBookmark, LucideCopy } from "lucide-react";
import { toast } from "sonner";
import { Extension } from "@codemirror/state";
import { languages } from "@codemirror/language-data";
import { cn } from "@/lib/utils";
import { LanguageIcon } from "./LanguageIcon";

interface SnippetCardProps extends ComponentProps<"div"> {
    snippet: Snippet
    saveCount?: number
    onSaveClick?: () => void
    isSaved?: boolean
}

const SnippetCard = ({snippet, saveCount, onSaveClick, isSaved = false, ...props}: SnippetCardProps) => {

    const [extensions, setExtensions] = useState<Extension[]>([]);

    useEffect(() => {
        const loadLanguage = async () => {
            const langName = snippet.language;
            
            const langDescription = languages.find((lang) => {
                return (
                    lang.name.toLowerCase() === langName.toLowerCase() ||
                    lang.alias.includes(langName.toLowerCase()) ||
                    lang.extensions.includes(langName.toLowerCase())
                );
            });

            if (langDescription) {
                const langSupport = await langDescription.load();
                setExtensions([langSupport]);
            } else {
                setExtensions([]);
            }
        };

        loadLanguage();
    }, [snippet.language]);


    return <Card className="shadow-none group cursor-pointer" {...props}>
        <CardContent>
            <div className="relative">
                <BaseCodeMirror
                    value={snippet.code}
                    readOnly
                    height="150px"
                    extensions={[extensions]}
                />
                <Button
                    onClick={(e) => {
                        e.stopPropagation()
                        navigator.clipboard.writeText(snippet.code)
                        toast("Snippet coppied to clipboard!", {
                            closeButton: true
                        })
                    }}
                    className="absolute top-2 right-2 opacity-0 group-hover:opacity-50 hover:opacity-100" 
                    variant={"outline"} 
                    size={"icon"}
                >
                    <LucideCopy/>
                </Button>
            </div>
        </CardContent>
        <CardHeader>
            <CardTitle className="flex gap-2">
                <span className="grow">{snippet.title}</span>
                <LanguageIcon className="text-muted-foreground" language={snippet.language}/>
            </CardTitle>
            <CardDescription>{snippet.description}</CardDescription>
        </CardHeader>
        <CardFooter className="flex gap-2 items-center">
            <Gravatar size={24} emailHash={snippet.author.email_hash}/>
            <span className="font-semibold">
                {snippet.author.username}
            </span>
            <span className="grow"/>
            { 
                saveCount !== undefined &&
                <span className="flex items-center font-mono text-amber-200">
                {saveCount}
                <Button variant={"ghost"} size={"icon-sm"} className="text-amber-300" onClick={(e) => {
                    e.stopPropagation()
                    onSaveClick?.()
                }}>
                    <LucideBookmark className={cn({"fill-amber-300":isSaved})}/>
                </Button>
            </span> }
                
            
        </CardFooter>
    </Card>
};

export default SnippetCard;
