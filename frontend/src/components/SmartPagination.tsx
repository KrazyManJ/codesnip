import { Pagination, PaginationContent, PaginationEllipsis, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "./ui/pagination";

interface SmartPaginationProps {
    currentPage: number
    pagesCount: number
    onNext: () => void
    onPrevious: () => void
    onExact: (value: number) => void
}

const SmartPagination = ({currentPage, pagesCount, onNext, onPrevious, onExact}: SmartPaginationProps) => {

    const minPageShown = Math.max(1,currentPage-1)
    const maxPageShown = Math.min(pagesCount,currentPage+1)

    const showElipsisStart = minPageShown !== 1
    const showElipsisEnd = maxPageShown !== currentPage
    
    const pagesNumbers = new Array(maxPageShown - minPageShown + 1).fill(0).map((_,i) => minPageShown+i)
    
    const showFirstPage = !pagesNumbers.includes(1)
    const showLastPage = !pagesNumbers.includes(pagesCount)

    return (
        <Pagination className="my-10">
            <PaginationContent>
                <PaginationItem>
                    <PaginationPrevious onClick={onPrevious}/>
                </PaginationItem>
                { showFirstPage && 
                    <PaginationItem>
                        <PaginationLink onClick={() => onExact(1)}>{1}</PaginationLink>
                    </PaginationItem>
                }
                { showElipsisStart &&<PaginationItem><PaginationEllipsis/></PaginationItem>}
                {
                    pagesNumbers.map(i => 
                        <PaginationItem key={i}>
                            <PaginationLink 
                                onClick={() => onExact(i)} 
                                isActive={i === currentPage}
                            >{i}</PaginationLink>
                        </PaginationItem>
                    )
                }
                { showElipsisEnd && <PaginationItem><PaginationEllipsis/></PaginationItem>}
                { showLastPage && 
                    <PaginationItem>
                        <PaginationLink onClick={() => onExact(pagesCount)}>{pagesCount}</PaginationLink>
                    </PaginationItem>
                }
                <PaginationItem>
                    <PaginationNext onClick={onNext}/>
                </PaginationItem>
            </PaginationContent>
        </Pagination>
    );
};

export default SmartPagination;
