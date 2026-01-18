import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function useAuthenticated(): boolean {
    const {data: session} = useSession()
    const router = useRouter()

    useEffect(() => {
        if (!session) {
            router.push("/")
        }
    }, [session, router])

    return !!session
}