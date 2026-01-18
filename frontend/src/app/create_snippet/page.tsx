"use client";

import { snippetApi } from "@/api";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import SnippetForm, { SnippetFormValues } from "@/components/SnippetForm";
import { useState } from "react";


export default function CreateSnippet() {

    const router = useRouter()
    const [submitState, setSubmitState] = useState(false)

    const handleCreate = async (data: SnippetFormValues) => {
        setSubmitState(true)
        try {
            await snippetApi.post("/snippets", data);
            router.back();
            toast("New snippet created");
        } catch {
            toast.error("Failed to create snippet")
        } finally {
            setSubmitState(false)
        }
    }

    return <main>
        <SnippetForm onSubmit={handleCreate} isSubmitting={submitState} />
    </main>
}