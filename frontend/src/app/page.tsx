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
import { parseAsInteger, useQueryState } from "nuqs"
import SmartPagination from "@/components/SmartPagination";
import { Skeleton } from "@/components/ui/skeleton";
import Repeater from "@/components/Repeater";

export default function Home() {

    const [pagesCount, setPagesCount] = useState(1)
    const [page, setPage] = useQueryState("page", parseAsInteger.withDefault(1))
    const [isLoading, setIsLoading] = useState(true)

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
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setIsLoading(true)
        snippetApi.get<PaginationResponse<Snippet>>("/snippets",{
            params: {
                size: 12,
                page: page
            }
        }).then(async (v) => {
            setSnippets(v.data.items)
            setPagesCount(v.data.pages)

            const {data: saves} = await savesApi.post<SavesBatchSingleSaveResponse[]>("/saves/stats/batch",{
                snippet_ids: v.data.items.map(v => v.id) 
            })
            saves.forEach(v => {
                saveCountMap.set(v.snippet_id, v.stats.save_count)
            })
            setIsLoading(false)
        })
        // snippetApi.get<string[]>("/langs").then(v => {
        //     setLangs(v.data)
        // })
    }, [saveCountMap, page])

    return (
        <main>
            <Banner/>
            <div className="flex justify-between py-6 gap-4">
                <SearchBar/>
                <Button onClick={() => router.push("create_snippet")}>
                    <LucidePlus size={20}/>
                    Create new
                </Button>
                
            </div>
            <div className="grid lg:grid-cols-3 gap-4 grid-cols-1">
                { !isLoading && snippets.map(v => 
                    <SnippetCard 
                        key={v.id} 
                        snippet={v} 
                        saveCount={saveCountMap.get(v.id) ?? 0}
                        onClick={() => router.push(`/snippet/${v.id}`)}
                        onSaveClick={() => handleSaveClick(v.id)}
                        isSaved={userSavedSnippetsIds.has(v.id)}
                    />
                )}
                { isLoading && <>
                    <Repeater n={12}>
                        <Skeleton className="w-full h-75"/>
                    </Repeater>
                </>}
            </div>
            <SmartPagination 
                currentPage={page} 
                pagesCount={pagesCount}
                onExact={(i) => setPage(i)}
                onPrevious={() => setPage(Math.max(1, page-1))}
                onNext={() => setPage(Math.min(pagesCount, page+1))}
            />
        </main>
    )
}

