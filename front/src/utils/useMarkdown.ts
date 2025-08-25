import MarkdownIt from 'markdown-it';

const md = new MarkdownIt({
    html: true,
    linkify: true,
    typographer: true,
    breaks: true,
});

export const parseMarkdown = (markdown: string): string => {
    return md.render(markdown ?? '');
};
