import { useEffect } from "react";
import { setBearerAuthToken } from "./api";
import { useSession } from "next-auth/react";

const TokenRefresher = () => {
    const { data: session } = useSession();

    useEffect(() => {
        if (session?.accessToken) {
            setBearerAuthToken(session.accessToken);
        } else {
            setBearerAuthToken(null);
        }
    }, [session]);

    return null;
};

export default TokenRefresher;
