"use client";

import { LucideCode2 } from "lucide-react";
import LoginButton from "./LoginButton";
import Link from "next/link";
import ThemeButton from "./ThemeButton";



const Header = () => {
    return <header className="bg-amber-400 text-primary-foreground">
        <div className="max-w-7xl mx-auto p-5 py-3 flex justify-between">
            <Link 
                href={{pathname: "/"}}
                className="flex gap-2 font-bold text-lg items-center select-none"
            >
                <LucideCode2 strokeWidth={2.5}/>
                <span>
                    <span className="font-mono">Code</span>
                    <span>Snip</span>
                </span>
            </Link>
            <div className="flex gap-4">
                <ThemeButton/>
                <LoginButton/>
            </div>
        </div>
    </header>
};

export default Header;
