"use client";

import { snippetApi } from '@/api';
import BaseCodeMirror from '@/components/BaseCodeMirror';
import { Button } from '@/components/ui/button';
import Snippet from '@/model/Snippet';
import { useSession } from 'next-auth/react';
import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { languages } from "@codemirror/language-data";
import { Extension } from '@codemirror/state';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { LucideBookmark, LucideCopy } from 'lucide-react';
import { toast } from 'sonner';
import Gravatar from '@/components/Gravatar';


export default function SnippetDetail() {
    const { id } = useParams();
    const { data: session } = useSession();
    const router = useRouter();

    const [snippet, setSnippet] = useState<Snippet>();
    const [extensions, setExtensions] = useState<Extension[]>([]);

    const isOwnSnippet = session?.user.id === snippet?.author.id

    useEffect(() => {
        snippetApi.get<Snippet>(`/snippets/${id}`).then(v => {
            setSnippet(v.data)
        })
    }, [id])

    const deleteSnippet = async () => {
        const {status} = await snippetApi.delete(`/snippets/${id}/`)
        if (status === 204) {
            router.back()
        }
    }

    useEffect(() => {
        if (!snippet) return;

        const loadLanguage = async () => {
            const langName = snippet?.language;
            
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
    }, [snippet]);

    if (!snippet) {
        return <main></main>
    }

    return (
        <main className='flex gap-5 grow'>
            <div className='w-full grow relative'>
                <BaseCodeMirror
                    value={snippet?.code}
                    extensions={extensions}
                    className='text-sm w-full h-full'
                    height='100%'
                />
                <Button
                    onClick={(e) => {
                        e.stopPropagation()
                        navigator.clipboard.writeText(snippet.code)
                        toast("Snippet coppied to clipboard!", {
                            closeButton: true,
                            position: "bottom-center"
                        })
                    }}
                    className="absolute top-2 right-2 bg-foreground opacity-50 hover:opacity-100" 
                    variant={"outline"} 
                    size={"icon"}
                >
                    <LucideCopy/>
                </Button>
            </div>
            <Card className='w-lg'>
                <CardHeader>
                    <CardTitle>{snippet.title}</CardTitle>
                    <CardDescription className='flex flex-col gap-4 mt-4'>
                        <div className='flex items-center gap-2'>
                            <Gravatar size={20} emailHash={snippet.author.email_hash}/>
                            <span>{snippet.author.username}</span>
                        </div>
                        <div>
                            {snippet.description}
                        </div>

                    </CardDescription>
                </CardHeader>
                <CardContent className='grow'>

                </CardContent>
                <CardFooter className='flex-col'>
                    {
                        !isOwnSnippet &&  
                            <div className='text-amber-200 font-mono flex w-full justify-end'>
                                <LucideBookmark className='text-amber-300'/>
                            </div>
                    }
                    <div className='flex flex-col gap-2 w-full'>
                        {isOwnSnippet && 
                            <>
                                <Button className='w-full' onClick={() => router.push(`/snippet/${id}/edit`)}>
                                    Edit
                                </Button>
                                <Button className='w-full' onClick={deleteSnippet} variant={"destructive"}>
                                    Remove
                                </Button>
                            </>
                        }
                    </div>
                </CardFooter>
            </Card>
        </main>
    )
}