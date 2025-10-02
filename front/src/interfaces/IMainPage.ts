import type { IReaction } from "./IEntities";

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

export interface SingleBlock {
  id: number;
  type: "swiper";
  title: string;
  images: ImageWithHref[];
  href?: string;
  modifiers?: string[];
}

export interface FullRowBlock {
  id: number;
  type: "section";
  title: string;
  href?: string;
  images: BlockImage[];
  sectionId: string;
}


export type MainPageBlock = SingleBlock | FullRowBlock ;
export type MainPageCards = MainPageBlock[];

export type IHomeViewSoloBlock = SingleBlock;