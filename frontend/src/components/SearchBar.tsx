import { useEffect, useState } from "react";
import {
    Command,
    CommandEmpty,
    CommandGroup,
    CommandInput,
    CommandItem,
    CommandList,
} from "./ui/command";
import { useDebounceValue } from "usehooks-ts"
import SearchEntry from "@/model/SearchEntry";
import { codesnipApi } from "@/api";
import HighlightedText from "./HighlightedText";
import { Spinner } from "./ui/spinner";
import { cn } from "@/lib/utils";
import { Decoration, DecorationSet, EditorView,  RangeSetBuilder, ViewPlugin, ViewUpdate } from "@uiw/react-codemirror";
import BaseCodeMirror from "./BaseCodeMirror";
import highlightPlugin from "@/lib/client/codemirror-highlight-plugin";





const SearchBar = () => {
    
    const [open, setOpen] = useState(false);
    const [searchInput, setSearchInput] = useState("")
    const [results, setResults] = useState<SearchEntry[]>([])
    const [isSearching, setIsSearching] = useState<boolean>(false)

    const [debouncedSearch, setDebouncedSearch] = useDebounceValue(searchInput, 500)
    
    useEffect(() => {
        setDebouncedSearch(searchInput);
        // eslint-disable-next-line react-hooks/set-state-in-effect
        setIsSearching(true);
    }, [searchInput, setDebouncedSearch])
    
    useEffect(() => {
        codesnipApi.post<SearchEntry[]>("/search", null, { params: { query: debouncedSearch } }).then(v => {
            setResults(v.data)
            setIsSearching(false)
        })
    }, [debouncedSearch])

    return (
        <div className="relative w-full overflow-visible">
            <Command 
                className={cn(" border overflow-visible z-50 transition-[border-radius]", {
                    "border-b-0 rounded-b-none duration-0": open
                })}
                shouldFilter={false}
            >
                <CommandInput 
                    placeholder="Search snippets..." 
                    onFocus={() => setOpen(true)} 
                    onBlur={() => setOpen(false)}
                    onValueChange={setSearchInput}
                    value={searchInput}
                    containerClassName="border-b-0"
                />

                {open && (
                    <div className="absolute top-full left-0 w-full bg-card rounded-b-md border outline-none animate-in fade-in-0 z-50">
                        <CommandList 
                            onMouseDown={(e) => e.preventDefault()}
                            className="max-h-75 overflow-y-auto"
                        >
                            <CommandEmpty className={cn({"flex w-full items-center justify-center": isSearching})}>
                                {isSearching ? <Spinner/> : <>No results found</>}
                            </CommandEmpty>
                            <CommandGroup>
                                {!isSearching && results.map((searchResult) => (
                                    <CommandItem
                                        key={searchResult.snippet.id}
                                        onSelect={() => {setOpen(false);}}
                                    >
                                        <div>
                                            <HighlightedText>{searchResult.match.title}</HighlightedText>
                                            <div>{`${!!searchResult.match.title}`}</div>
                                        </div>
                                        <div>
                                            <HighlightedText>{searchResult.match.description}</HighlightedText>
                                        </div>
                                        {
                                            searchResult.match.code && <BaseCodeMirror
                                                value={searchResult.match.code}
                                                extensions={[highlightPlugin]}
                                            />
                                        }
                                    </CommandItem>
                                ))}
                            </CommandGroup>
                        </CommandList>
                    </div>
                )}
            </Command>
        </div>
    );
};

export default SearchBar;
