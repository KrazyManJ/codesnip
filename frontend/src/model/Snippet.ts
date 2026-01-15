import UploadSnippet from "./UploadSnippet"

export default interface Snippet extends UploadSnippet {
    id: string
    author: {
        id: string
        username: string
        email_hash: string
    }
    created_at: string
}