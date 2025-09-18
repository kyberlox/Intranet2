import type { IReaction } from "./IEntities";

// Common image types
export interface ImageWithHref {
  id: number;
  image: string;
  title?: string;
  href?: string;
  reactions?: IReaction;
  blockTitle?: string;
}

export interface BlockImage {
  id: number;
  title?: string;
  description?: string;
  image: string;
  href?: string;
  reactions?: IReaction;
  blockTitle?: string;
}

// Top-level blocks
export interface SingleBlock {
  id: number;
  type: "singleBlock";
  title: string;
  images: ImageWithHref[];
  href?: string;
  modifiers?: string[];
}

export interface FullRowBlock {
  id: number;
  type: "fullRowBlock";
  title: string;
  href?: string;
  images: BlockImage[];
  sectionId: string;
}

// Mixed row block content (discriminated union)
export interface MixedRowSingleBlockContent {
  id?: number;
  type: "singleBlock";
  title: string;
  images: ImageWithHref[]; // only ImageWithHref for single-block content
  href?: string;
  modifiers?: string[];
  blockTitle?: string;
}

export interface MixedRowFullRowBlockContent {
  id?: number;
  type: "fullRowBlock";
  title: string;
  images: BlockImage[]; 
  href?: string;
  sectionId?: string;
  blockTitle?: string;
}

export type MixedRowBlockContent =
  | MixedRowSingleBlockContent
  | MixedRowFullRowBlockContent;

export interface MixedRowBlock {
  id: number;
  type: "mixedRowBlock";
  content: MixedRowBlockContent[];
}

export type MainPageBlock = SingleBlock | FullRowBlock | MixedRowBlock;
export type MainPageCards = MainPageBlock[];

export type IHomeViewSoloBlock = SingleBlock;