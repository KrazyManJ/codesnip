import { cn } from "@/lib/utils";
import { duotoneLight, duotoneDark } from "@uiw/codemirror-theme-duotone";
import ReactCodeMirror, { EditorView, ReactCodeMirrorProps } from "@uiw/react-codemirror";
import { useTheme } from "next-themes";

const BaseCodeMirror = ({extensions = [], className, ...props}: ReactCodeMirrorProps) => {

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

    return <ReactCodeMirror
        theme={resolvedTheme === "light" ? duotoneLight : duotoneDark}
        className={cn("rounded-lg overflow-hidden border border-border text-xs", className)}
        extensions={[
            tweakTheme,
            ...extensions
        ]}
        {...props}
    />;
};

export default BaseCodeMirror;
