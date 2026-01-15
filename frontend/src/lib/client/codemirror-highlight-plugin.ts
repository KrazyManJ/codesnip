import {
    Decoration,
    DecorationSet,
    EditorView,
    RangeSetBuilder,
    ViewPlugin,
    ViewUpdate,
} from "@uiw/react-codemirror";

const highlightMark = Decoration.mark({ class: "bg-amber-300" });
const hideToken = Decoration.replace({});

const highlightPlugin = ViewPlugin.fromClass(
    class {
        decorations: DecorationSet;

        constructor(view: EditorView) {
            this.decorations = this.getDecorations(view);
        }

        update(update: ViewUpdate): void {
            if (update.docChanged || update.viewportChanged) {
                this.decorations = this.getDecorations(update.view);
            }
        }

        private getDecorations(view: EditorView): DecorationSet {
            const builder = new RangeSetBuilder<Decoration>();
            const regex = /(<{%HL_START%}>)(.*?)(<{%HL_END%}>)/g;
            const text = view.state.doc.toString();

            for (const { from, to } of view.visibleRanges) {
                const section = text.slice(from, to);
                let match: RegExpExecArray | null;

                while ((match = regex.exec(section)) !== null) {
                    const startMatch = from + match.index;
                    const startTokenEnd = startMatch + match[1].length;
                    const contentEnd = startTokenEnd + match[2].length;
                    const totalEnd = startMatch + match[0].length;

                    builder.add(startMatch, startTokenEnd, hideToken);
                    builder.add(startTokenEnd, contentEnd, highlightMark);
                    builder.add(contentEnd, totalEnd, hideToken);
                }
            }
            return builder.finish();
        }
    },
    {
        decorations: (v) => v.decorations,
    }
);

export default highlightPlugin;