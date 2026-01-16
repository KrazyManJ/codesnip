"use client";

import { savesApi, snippetApi } from "@/api";
import Banner from "@/components/Banner";
import { LanguageIcon } from "@/components/LanguageIcon";
import SearchBar from "@/components/SearchBar";
import SnippetCard from "@/components/SnippetCard";
import { Button } from "@/components/ui/button";
import { Pagination, PaginationContent, PaginationEllipsis, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "@/components/ui/pagination";
import PaginationResponse from "@/model/PaginationResponse";
import SavesBatchSingleSaveResponse from "@/model/SavesBatchSingleSaveResponse";
import Snippet from "@/model/Snippet";
import { LucidePlus } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Home() {
    const [snippets, setSnippets] = useState<Snippet[]>([])
    // const [langs, setLangs] = useState<string[]>([])
    const [saveData, setSaveData] = useState<SavesBatchSingleSaveResponse[]>([])
    const router = useRouter()


    useEffect(() => {
        snippetApi.get<PaginationResponse<Snippet>>("/snippets",{
            params: {
                size: 50
            }
        }).then(async (v) => {
            console.log(v.data)
            setSnippets(v.data.items)

            const {data: saves} = await savesApi.post<SavesBatchSingleSaveResponse[]>("/saves/stats/batch",{
                snippet_ids: v.data.items.map(v => v.id) 
            })
            setSaveData(saves)
            console.log(saves)
        })
        // snippetApi.get<string[]>("/langs").then(v => {
        //     setLangs(v.data)
        // })
        
    }, [])

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
                        saveCount={saveData.find(f => f.snippet_id == v.id)?.stats?.save_count ?? 0}
                        onClick={() => router.push(`/snippet/${v.id}`)}
                    />
                )}
            </div>
            <Pagination className="my-10">
                <PaginationContent>
                    <PaginationItem>
                        <PaginationPrevious/>
                    </PaginationItem>
                    <PaginationItem>
                        <PaginationLink>1</PaginationLink>
                    </PaginationItem>
                    <PaginationItem>
                        <PaginationLink>2</PaginationLink>
                    </PaginationItem>
                    <PaginationItem>
                        <PaginationEllipsis/>
                    </PaginationItem>
                    <PaginationItem>
                        <PaginationNext/>
                    </PaginationItem>
                </PaginationContent>
            </Pagination>
        </main>
    )
}

