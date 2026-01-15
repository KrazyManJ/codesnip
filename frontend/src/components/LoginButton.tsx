import { useFederatedLogout } from "@/hooks/useFederatedLogout";
import { LucideLogIn, LucideLogOut } from "lucide-react";
import { signIn, useSession } from "next-auth/react";
import React from "react";
import Gravatar from "./Gravatar";

const LoginButton = () => {
    const { data: session } = useSession();
    const signOut = useFederatedLogout()


    if (session) return <span className="flex gap-2 items-center select-none">
        <Gravatar size={32} email={session.user.email ?? ""}/>
        <span className="font-semibold">
            {session.user.name}
        </span>
        <button 
            onClick={() => signOut()}
            className="cursor-pointer"
        >
            <LucideLogOut size={20} className="text-red-600"/>
        </button>
    </span>

    return <span 
        className="flex gap-2 items-center cursor-pointer select-none"
        onClick={() => signIn("keycloak")}
    >
        Login
        <button
            onClick={() => signIn("keycloak")} 
        >
            <LucideLogIn size={20}/>
        </button>
    </span>
};

export default LoginButton;
