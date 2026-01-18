import Snippet from "@/model/Snippet";
import { ComponentProps } from "react";
import { Field, FieldError, FieldGroup, FieldLabel } from "./ui/field";
import { Button } from "./ui/button";
import { Select, SelectContent, SelectGroup, SelectItem, SelectLabel, SelectTrigger, SelectValue } from "./ui/select";
import { LucideEye, LucideLock } from "lucide-react";
import { Controller, useForm } from "react-hook-form";
import z from "../../node_modules/zod/v4/classic/external.cjs";
import { zodResolver } from "@hookform/resolvers/zod";
import { Input } from "./ui/input";
import { Textarea } from "./ui/textarea";
import BaseCodeMirror from "./BaseCodeMirror";
import { Spinner } from "./ui/spinner";


const formSchema = z.object({
    title: z.string().min(1, "Cannot be empty"),
    description: z.string(),
    code: z.string().min(1, "Cannot be empty"),
    language: z.string().min(1, "Cannot be empty"),
    visibility: z.enum(["public", "private"])
})

export type SnippetFormValues = z.infer<typeof formSchema>


interface SnippetFormProps extends Omit<ComponentProps<"form">, "onSubmit"> {
    initialSnippet?: Snippet
    onSubmit: (snippet: SnippetFormValues) => void
    isSubmitting: boolean
}


const SnippetForm = ({ initialSnippet, onSubmit, isSubmitting }: SnippetFormProps) => {


    const form = useForm<SnippetFormValues>({
        resolver: zodResolver(formSchema),
        mode: "onChange",
        defaultValues: initialSnippet || {
            title: "",
            description: "",
            code: "",
            language: "",
            visibility: "public"
        }
    })


    return (
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
                            <BaseCodeMirror
                                {...field}
                                height="150px"
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
                    <Button type="submit" disabled={!form.formState.isValid || isSubmitting}>
                        {isSubmitting && <Spinner/>}
                        {!isSubmitting && !initialSnippet &&  "Create"}
                        {isSubmitting && !initialSnippet && "Creating..."}
                        {!isSubmitting && initialSnippet && "Edit"}
                        {isSubmitting && initialSnippet && "Editing..."}
                    </Button>
                </Field>
            </FieldGroup>
        </form>
    );
};

export default SnippetForm;
