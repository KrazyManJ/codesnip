"use client";

import { savesApi, snippetApi } from "@/api";
import SnippetCard from "@/components/SnippetCard";
import PaginationResponse from "@/model/PaginationResponse";
import Save from "@/model/Save";
import Snippet from "@/model/Snippet";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";


export default function ProfilePage() {
    
    const { data: session } = useSession()
    const router = useRouter()

    const [userSnippets, setUserSnippets] = useState<PaginationResponse<Snippet>>()
    const [savedSnippets, setSavedSnippets] = useState<Snippet[]>([])
    
    const getSavedSnippets = async () => {
        const {data: saves} = await savesApi.get<PaginationResponse<Save>>("/saves/me", { params: {
            size: 9
        }})
        const {data: snippets} = await snippetApi.post<Snippet[]>("/snippets/batch", {
            snippet_ids: saves.items.map(v => v.snippet_id)
        })
        setSavedSnippets(snippets)
    }

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        getSavedSnippets()
    }, [])

    useEffect(() => {
        snippetApi.get<PaginationResponse<Snippet>>("/snippets/me").then((v) => setUserSnippets(v.data))
    }, [userSnippets])

    return (
        <main>
            <h2 className="text-xl font-bold mb-4">My Snippets</h2>
            <div className="grid lg:grid-cols-3 gap-4 grid-cols-1">
                { userSnippets?.items.map(snippet => 
                    <SnippetCard 
                    snippet={snippet} 
                    key={snippet.id}
                    onClick={() => router.push(`/snippet/${snippet.id}`)}
                    />
                ) }
            </div>
            <h2 className="text-xl font-bold mt-16 mb-4">Saved Snippets</h2>
            <div className="grid lg:grid-cols-3 gap-4 grid-cols-1">
                { savedSnippets.map(snippet => 
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