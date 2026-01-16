"use client";

import { snippetApi } from "@/api";
import SnippetCard from "@/components/SnippetCard";
import PaginationResponse from "@/model/PaginationResponse";
import Snippet from "@/model/Snippet";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";


export default function ProfilePage() {
    
    const { data: session } = useSession()
    const router = useRouter()

    const [userSnippets, setUserSnippets] = useState<PaginationResponse<Snippet>>()
    

    useEffect(() => {
        snippetApi.get<PaginationResponse<Snippet>>("/snippets/me").then((v) => setUserSnippets(v.data))
    }, [userSnippets])

    return (
        <main>
            <div className="grid grid-cols-3">
                { userSnippets?.items.map(snippet => 
                    <SnippetCard 
                        snippet={snippet} 
                        key={snippet.id}
                        onClick={() => router.push(`/snippet/${snippet.id}`)}
                    />
                ) }
            </div>
        </main>
    )
}