interface HighlightedTextProps {
    children: string;
}

const HighlightedText = ({ children }: HighlightedTextProps) => {
    if (!children) return null;

    const parts = children.split(/(<{%HL_START%}>.*?<{%HL_END%}>)/g);

    return (
        <span>
            {parts.map((part, index) => {
                if (
                    part.startsWith("<{%HL_START%}>") &&
                    part.endsWith("<{%HL_END%}>")
                ) {
                    const content = part
                        .replace("<{%HL_START%}>", "")
                        .replace("<{%HL_END%}>", "");

                    return (
                        <mark key={index} className="bg-amber-300">
                            {content}
                        </mark>
                    );
                }

                return part;
            })}
        </span>
    );
};

export default HighlightedText;
