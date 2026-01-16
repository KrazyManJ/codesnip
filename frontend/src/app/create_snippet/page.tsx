"use client";

import { snippetApi } from "@/api";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import SnippetForm, { SnippetFormValues } from "@/components/SnippetForm";
import { useBoolean } from "usehooks-ts";


export default function CreateSnippet() {

    const router = useRouter()
    const submitState = useBoolean()

    const handleCreate = async (data: SnippetFormValues) => {
        submitState.setTrue()
        try {
            await snippetApi.post("/snippets", data);
            router.push("/");
            toast("New snippet created");
        } catch {
            toast.error("Failed to create snippet")
        } finally {
            submitState.setFalse()
        }
    }

    return <main>
        <SnippetForm onSubmit={handleCreate} isSubmitting={submitState.value} />
    </main>
}