export default interface PaginationResponse<T> {
    items: T[];
    total: number;
    page: number;
    size: number;
    pages: number;
}