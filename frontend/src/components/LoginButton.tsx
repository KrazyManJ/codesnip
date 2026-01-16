import { useFederatedLogout } from "@/hooks/useFederatedLogout";
import { LucideLogIn, LucideLogOut } from "lucide-react";
import { signIn, useSession } from "next-auth/react";
import React from "react";
import Gravatar from "./Gravatar";
import { Button } from "./ui/button";
import Link from "next/link";

const LoginButton = () => {
    const { data: session } = useSession();
    const signOut = useFederatedLogout()


    if (session) return <span className="flex gap-2 items-center select-none">
        <Link className="font-semibold flex items-center gap-2" href={`/profile`}>
            <Gravatar size={32} email={session.user.email ?? ""}/>
            {session.user.name}
        </Link>
        <Button
            onClick={() => signOut()}
        >
            <LucideLogOut size={20} className="text-red-600"/>
        </Button>
    </span>

    return <span 
        className="flex gap-2 items-center cursor-pointer select-none"
        onClick={() => signIn("keycloak")}
    >
        <Button
            className="flex items-center gap-2"
            onClick={() => signIn("keycloak")} 
        >
            Login
            <LucideLogIn size={20}/>
        </Button>
    </span>
};

export default LoginButton;
