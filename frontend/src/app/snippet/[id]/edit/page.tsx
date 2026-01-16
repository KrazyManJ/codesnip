"use client";

import { snippetApi } from "@/api";
import SnippetForm, { SnippetFormValues } from "@/components/SnippetForm";
import Snippet from "@/model/Snippet";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { useBoolean } from "usehooks-ts";

export default function EditPage() {
    
    const { id } = useParams();
    const router = useRouter();
    const submitState = useBoolean();

    const [snippet, setSnippet] = useState<Snippet>()

    useEffect(() => {
        snippetApi.get(`/snippets/${id}`).then((v) => {
            setSnippet(v.data)
        })
    }, [id])

    const handleCreate = async (data: SnippetFormValues) => {
        submitState.setTrue()
        try {
            await snippetApi.put(`/snippets/${id}`, data);
            router.push("/");
            toast("Snippet Updated");
        } catch {
            toast.error("Failed to create snippet")
        } finally {
            submitState.setFalse()
        }
    }
    

    return (
        <main>
            {
                snippet != null && <SnippetForm onSubmit={handleCreate} isSubmitting={submitState.value} initialSnippet={snippet}/>
            }
        </main>
    )
}