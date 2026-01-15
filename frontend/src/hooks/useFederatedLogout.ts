import { signOut, useSession } from "next-auth/react";
import { useRouter } from "next/navigation";

export const useFederatedLogout = () => {
    const { data: session } = useSession();
    const router = useRouter();

    const federatedLogout = async () => {
        try {
            if (!session?.idToken) {
                await signOut();
                return;
            }

            const params = new URLSearchParams({
                client_id: process.env.NEXT_PUBLIC_KEYCLOAK_CLIENT_ID as string,
                id_token_hint: session.idToken,
                post_logout_redirect_uri: window.location.origin,
            });

            const logoutUrl = `${
                process.env.NEXT_PUBLIC_KEYCLOAK_ISSUER
            }/protocol/openid-connect/logout?${params.toString()}`;

            await signOut({ redirect: false });
            router.push(logoutUrl);
        } catch (error) {
            console.error("Logout error:", error);
        }
    };

    return federatedLogout;
};
