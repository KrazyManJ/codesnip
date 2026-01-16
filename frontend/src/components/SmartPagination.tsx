import { Pagination, PaginationContent, PaginationEllipsis, PaginationItem, PaginationLink, PaginationNext, PaginationPrevious } from "./ui/pagination";

interface SmartPaginationProps {
    currentPage: number
    onNext: () => void
    onPrevous: () => void
    onExact: () => void
}

const SmartPagination = ({}: SmartPaginationProps) => {
    return (
        <Pagination className="my-10">
            <PaginationContent>
                <PaginationItem>
                    <PaginationPrevious/>
                </PaginationItem>
                <PaginationItem>
                    <PaginationLink href="#">1</PaginationLink>
                </PaginationItem>
                <PaginationItem>
                    <PaginationLink>2</PaginationLink>
                </PaginationItem>
                <PaginationItem>
                    <PaginationEllipsis/>
                </PaginationItem>
                <PaginationItem>
                    <PaginationNext/>
                </PaginationItem>
            </PaginationContent>
        </Pagination>
    );
};

export default SmartPagination;
