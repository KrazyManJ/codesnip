"use client";

import { snippetApi } from '@/api';
import { Button } from '@/components/ui/button';
import Snippet from '@/model/Snippet';
import { useSession } from 'next-auth/react';
import { useParams, useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';


export default function SnippetDetail() {
    const { id } = useParams();
    const { data: session } = useSession();
    const router = useRouter();

    const [snippet, setSnippet] = useState<Snippet>()

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

    return (
        <main>
            Snippet id: {id}
            <div>{snippet?.title}</div>
            <div>
                {session?.user.id === snippet?.author.id && 
                    <>
                        <Button onClick={() => router.push(`/snippet/${id}/edit`)}>
                            Edit
                        </Button>
                        <Button onClick={deleteSnippet}>
                            Remove
                        </Button>
                    </>
                }
            </div>
        </main>
    )
}