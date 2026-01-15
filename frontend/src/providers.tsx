"use client";

import { SessionProvider } from "next-auth/react";
import { ReactNode } from "react";
import TokenRefresher from "./TokenRefresher";
import { ThemeProvider } from "next-themes"
import { Toaster } from "sonner";

interface Props {
    children: ReactNode;
}

export const Providers = ({ children }: Props) => {
    return <ThemeProvider attribute={"class"}>
        <SessionProvider>
            <TokenRefresher/>
            {children}
            <Toaster className="bg-amber-400" />
        </SessionProvider>
    </ThemeProvider>
};
