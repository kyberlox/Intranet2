import type { Component } from "vue";

export interface ITrainingSections {
    name: string;
    link: string;
    component: Component | string;
}