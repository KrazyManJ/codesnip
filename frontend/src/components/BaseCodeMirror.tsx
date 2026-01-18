import { cn } from "@/lib/utils";
import { duotoneLight, duotoneDark } from "@uiw/codemirror-theme-duotone";
import ReactCodeMirror, { EditorView, Extension, ReactCodeMirrorProps } from "@uiw/react-codemirror";
import { useTheme } from "next-themes";
import { useMemo } from "react";


interface BaseCodeMirrorProps extends ReactCodeMirrorProps {
    disableScroll?: boolean
}


const BaseCodeMirror = ({disableScroll = false, extensions = [], className, ...props}: BaseCodeMirrorProps) => {

    const { resolvedTheme } = useTheme()

    const tweakTheme = EditorView.theme({
        ".cm-scroller": { 
            fontFamily: `var(--font-mono) !important`
        },
        ".cm-activeLine": {
            backgroundColor: "transparent !important"
        },
        ".cm-activeLineGutter": {
            backgroundColor: "transparent !important"
        }
    });

    const hideScrollTheme = EditorView.theme({
        ".cm-scroller": { overflow: "hidden" }
    });

    const extensionMemo = useMemo<Extension[]>(() => {
        const exts = [tweakTheme]
        if (disableScroll) {
            exts.push(hideScrollTheme)
        }
        return [...exts, ...extensions]
    }, [disableScroll, extensions, hideScrollTheme, tweakTheme])

    return <ReactCodeMirror
        theme={resolvedTheme === "light" ? duotoneLight : duotoneDark}
        className={cn("rounded-lg overflow-hidden border border-border text-xs", className)}
        extensions={extensionMemo}
        {...props}
    />;
};

export default BaseCodeMirror;
