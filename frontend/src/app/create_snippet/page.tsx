"use client";

import { codesnipApi } from "@/api";
import { Field, FieldError, FieldGroup, FieldLabel } from "@/components/ui/field";
import { Input } from "@/components/ui/input";
import ReactCodeMirror, { EditorView } from "@uiw/react-codemirror";
import { useRouter } from "next/navigation";
import { Controller, useForm } from "react-hook-form";
import z from "zod";
import { zodResolver } from "@hookform/resolvers/zod"
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "@/components/ui/select";
import { LucideEye, LucideLock } from "lucide-react";
import { duotoneLight, duotoneDark } from "@uiw/codemirror-theme-duotone";
import { useTheme } from "next-themes";
import { toast } from "sonner";


const formSchema = z.object({
    title: z.string()
        .min(1, "Cannot be empty")
        ,
    description: z.string(),
    code: z.string().min(1, "Cannot be empty"),
    language: z.string().min(1, "Cannot be empty"),
    visibility: z.enum(["public", "private"])
})

type FormValues = z.infer<typeof formSchema>

export default function CreateSnippet() {

    const router = useRouter()
    const { resolvedTheme } = useTheme()

    const transparentTheme = EditorView.theme({
        ".cm-scroller": { 
            fontFamily: `var(--font-mono) !important`
        },
        ".cm-activeLine": {
            backgroundColor: "transparent !important"
        },
        ".cm-activeLineGutter": {
            backgroundColor: "transparent !important"
        }
    });
    
    const form = useForm<FormValues>({
        resolver: zodResolver(formSchema),
        mode: "onChange",
        defaultValues: {
            title: "",
            description: "",
            code: "",
            language: "",
            visibility: "public"
        }
    })

    const onSubmit = (data: FormValues) => {
        codesnipApi.post("/snippets", data)
        router.push("/")
        toast("New snippet created!")
    }
    
    return <main>
        <form onSubmit={form.handleSubmit(onSubmit)}>
            <FieldGroup>
                <Controller
                    name="title"
                    control={form.control}
                    render={({ field, fieldState }) => (
                        <Field>
                            <FieldLabel>Title</FieldLabel>
                            <Input 
                                {...field}
                                id="codesnip-snippet-title"
                                aria-invalid={fieldState.invalid}
                                placeholder="Title"
                                autoComplete="off"
                                />
                            {fieldState.invalid && (
                                <FieldError errors={[fieldState.error]} />
                            )}
                        </Field>
                    )}
                />
                <Controller
                    name="description"
                    control={form.control}
                    render={({ field, fieldState }) => (
                        <Field>
                            <FieldLabel>Description</FieldLabel>
                            <Textarea 
                                {...field}
                                id="codesnip-snippet-title"
                                aria-invalid={fieldState.invalid}
                                placeholder="Description"
                                autoComplete="off"
                            />
                            {fieldState.invalid && (
                                <FieldError errors={[fieldState.error]} />
                            )}
                        </Field>
                    )}
                />
                <Controller
                    name="code"
                    control={form.control}
                    render={({ field, fieldState}) => (
                        <Field>
                            <FieldLabel>Code</FieldLabel>
                            <ReactCodeMirror
                                {...field}
                                extensions={[transparentTheme]}
                                height="150px"
                                className="text-sm overflow-hidden border border-border rounded-lg"
                                theme={resolvedTheme === "light" ? duotoneLight : duotoneDark}
                            />
                            {fieldState.invalid && (
                                <FieldError errors={[fieldState.error]} />
                            )}
                        </Field>
                    )}
                />
                <Controller
                    name="language"
                    control={form.control}
                    render={({ field, fieldState }) => (
                        <Field>
                            <FieldLabel>Language</FieldLabel>
                            <Input 
                                {...field}
                                id="codesnip-snippet-language"
                                aria-invalid={fieldState.invalid}
                                placeholder="Language"
                                autoComplete="off"
                            />
                            {fieldState.invalid && (
                                <FieldError errors={[fieldState.error]} />
                            )}
                        </Field>
                    )}
                />
                <Controller
                    name="visibility"
                    control={form.control}
                    render={({ field, fieldState }) => (
                        <Field>
                            <FieldLabel>Visibility</FieldLabel>
                            <Select
                                value={field.value}
                                onValueChange={field.onChange}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Visibility"/>
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectGroup>
                                        <SelectLabel>Visibility</SelectLabel>
                                        <SelectItem value="public"><LucideEye/>Public</SelectItem>
                                        <SelectItem value="private"><LucideLock/>Private</SelectItem>
                                    </SelectGroup>
                                </SelectContent>
                            </Select>
                            {fieldState.invalid && (
                                <FieldError errors={[fieldState.error]} />
                            )}
                        </Field>
                    )}
                />

                <Field>
                    <Button type="submit" disabled={!form.formState.isValid}>
                        Create
                    </Button>
                </Field>
            </FieldGroup>
        </form>
    </main>
}