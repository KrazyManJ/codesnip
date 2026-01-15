"use client";

import { codesnipApi } from "@/api";
import Banner from "@/components/Banner";
import SearchBar from "@/components/SearchBar";
import SnippetCard from "@/components/SnippetCard";
import { Button } from "@/components/ui/button";
import PaginationResponse from "@/model/PaginationResponse";
import Snippet from "@/model/Snippet";
import { LucidePlus } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

export default function Home() {
    const [snippets, setSnippets] = useState<Snippet[]>([])
    const router = useRouter()


    useEffect(() => {
        codesnipApi.get<PaginationResponse<Snippet>>("/snippets").then(v => {
            console.log(v)
            setSnippets(v.data.items)
        })
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
                {snippets.map(v => <SnippetCard key={v.id} snippet={v}/>)}
            </div>
        </main>
    )
}

