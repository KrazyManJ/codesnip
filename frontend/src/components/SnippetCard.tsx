import Snippet from "@/model/Snippet";
import { ComponentProps } from "react";
import Gravatar from "./Gravatar";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "./ui/card";
import BaseCodeMirror from "./BaseCodeMirror";
import { Button } from "./ui/button";
import { LucideBookmark, LucideCopy } from "lucide-react";
import { toast } from "sonner";

interface SnippetCardProps extends ComponentProps<"div"> {
    snippet: Snippet
}

const SnippetCard = ({snippet}: SnippetCardProps) => {
    return <Card className="shadow-none group">
        <CardContent>
            <div className="relative">
                <BaseCodeMirror
                    value={snippet.code}
                    readOnly
                    height="150px" 
                />
                <Button
                    onClick={() => {
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
            <CardTitle>{snippet.title}</CardTitle>
            <CardDescription>{snippet.description}</CardDescription>
        </CardHeader>
        <CardFooter className="flex gap-2 items-center">
            <Gravatar size={24} emailHash={snippet.author.email_hash}/>
            <span className="font-semibold">
                {snippet.author.username}
            </span>
            <span className="grow"/>
            <Button variant={"ghost"} size={"icon-sm"} className="text-amber-300">
                <LucideBookmark/>
            </Button>
        </CardFooter>
    </Card>
};

export default SnippetCard;
