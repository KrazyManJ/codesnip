export default interface SearchEntry {
    snippet: {
        id: string;
        title: string;
        language: string;
    };
    match: {
        title: string;
        description: string;
        code: string;
    };
}
