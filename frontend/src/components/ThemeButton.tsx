"use client";

import { useTheme } from "next-themes";
import { Button } from "./ui/button";
import { LucideMonitorSmartphone, LucideMoon, LucideSun } from "lucide-react";
import { useIsMounted } from "usehooks-ts";

const ThemeButton = () => {
    
    const { theme, setTheme } = useTheme()
    const isMounted = useIsMounted()
    
    const cycleTheme = () => {
        if (theme === "system") setTheme("dark")
        else if (theme === "dark") setTheme("light")
        else if (theme === "light") setTheme("system")
    }

    if (!isMounted()) {
        return <Button 
            onClick={cycleTheme} 
            className="cursor-pointer text-primary-foreground"
        >
            <LucideMonitorSmartphone/>
        </Button>
    }
    
    return <Button onClick={cycleTheme} className="cursor-pointer text-primary-foreground">
        {theme === "system" && <LucideMonitorSmartphone/> }
        {theme === "dark" && <LucideMoon/> }
        {theme === "light" && <LucideSun/> }
    </Button>;
};

export default ThemeButton;
