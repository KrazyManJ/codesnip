export default interface UploadSnippet {
    title: string
    description: string
    code: string
    language: string
    visibility: "public" | "private"
}