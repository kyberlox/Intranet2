<template><!-- Yandex.Metrika counter -->
<div><img src="https://mc.yandex.ru/watch/104472774"
         style="position:absolute; left:-9999px;"
         alt="" /></div>
<!-- /Yandex.Metrika counter -->
</template>
<script lang="ts">
// @ts-nocheck
import { defineComponent } from "vue";
export default defineComponent({
    props: {
        uid: {
            type: Number
        }
    },
    setup(props) {
        const ymKey = Number(import.meta.env.YMETRIKA_KEY);
        (function (m, e, t, r, i, k, a) {
            m[i] = m[i] || function () { (m[i].a = m[i].a || []).push(arguments) };
            m[i].l = 1 * new Date();
            for (var j = 0; j < document.scripts.length; j++) { if (document.scripts[j].src === r) { return; } }
            k = e.createElement(t), a = e.getElementsByTagName(t)[0], k.async = 1, k.src = r, a.parentNode.insertBefore(k, a)
        })
            (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

        ym(ymKey, "init", {
            clickmap: true,
            trackLinks: true,
            accurateTrackBounce: true,
            webvisor: true,
            userParams: {
                UserID: props.uid
            }
        });

        watch((props), () => {
            if (props.uid) {
                ym(ymKey, 'setUserID', props.uid);
            }
            console.log('ym', props.uid);
        })

        return {
        }
    }
})
</script>