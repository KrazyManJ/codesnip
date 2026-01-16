"use client";

import { savesApi, snippetApi } from "@/api";
import Banner from "@/components/Banner";
import SearchBar from "@/components/SearchBar";
import SnippetCard from "@/components/SnippetCard";
import { Button } from "@/components/ui/button";
import PaginationResponse from "@/model/PaginationResponse";
import SavesBatchSingleSaveResponse from "@/model/SavesBatchSingleSaveResponse";
import Snippet from "@/model/Snippet";
import { LucidePlus } from "lucide-react";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { useSet, useMap } from "@uidotdev/usehooks"
import { useSession } from "next-auth/react";

export default function Home() {

    const [snippets, setSnippets] = useState<Snippet[]>([])
    const saveCountMap = useMap() as Map<string, number>
    const userSavedSnippetsIds = useSet<string>()
    const router = useRouter()
    const { data: session } = useSession()


    const loadSavesData = useCallback(async () => {
        const { data } = await savesApi.post<{ snippet_id: string }[]>("/saves/check-status", {
            snippet_ids: snippets.map(v => v.id)
        })
        userSavedSnippetsIds.clear()
        data.forEach(v => userSavedSnippetsIds.add(v.snippet_id))
    }, [snippets, userSavedSnippetsIds])

    const handleSaveClick = async (snippet_id: string) => {
        console.log("Test")
        if (userSavedSnippetsIds.has(snippet_id)) {
            await savesApi.delete(`/saves/${snippet_id}`)
            saveCountMap.set(snippet_id, saveCountMap.get(snippet_id)!-1)
        }
        else {
            await savesApi.post("/saves", { snippet_id: snippet_id })
            saveCountMap.set(snippet_id, (saveCountMap.get(snippet_id) ?? 0) + 1)
        }
        await loadSavesData()
    }

    useEffect(() => {
        const loadUserData = async () => {
            await loadSavesData()
        }

        if (!session) return;
        loadUserData()
    }, [session, loadSavesData])

    useEffect(() => {
        snippetApi.get<PaginationResponse<Snippet>>("/snippets",{
            params: {
                size: 10
            }
        }).then(async (v) => {
            setSnippets(v.data.items)

            const {data: saves} = await savesApi.post<SavesBatchSingleSaveResponse[]>("/saves/stats/batch",{
                snippet_ids: v.data.items.map(v => v.id) 
            })
            saves.forEach(v => {
                saveCountMap.set(v.snippet_id, v.stats.save_count)
            })
        })
        // snippetApi.get<string[]>("/langs").then(v => {
        //     setLangs(v.data)
        // })
    }, [saveCountMap])

    return (
        <main>
            <Banner/>
            <div className="flex justify-between py-6 gap-4">
                <SearchBar/>
                <Button
                    onClick={() => router.push("create_snippet")}
                >
                    <LucidePlus size={20}/>
                    Create new
                </Button>
                
            </div>
            <div className="grid grid-cols-3 gap-4">
                { snippets.map(v => 
                    <SnippetCard 
                        key={v.id} 
                        snippet={v} 
                        saveCount={saveCountMap.get(v.id) ?? 0}
                        onClick={() => router.push(`/snippet/${v.id}`)}
                        onSaveClick={() => handleSaveClick(v.id)}
                        isSaved={userSavedSnippetsIds.has(v.id)}
                    />
                )}
            </div>
        </main>
    )
}

