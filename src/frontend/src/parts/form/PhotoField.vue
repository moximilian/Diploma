<template>
    <div>
        <img
            :src="src ? `data:image/png;base64,${src}` : defaultSrc"
            alt="photo"
            :class="className"
        />
    </div>
</template>

<script>
import { BASE_URL } from '@/api/api.settings'
export default {
    data() {
        return {
            defaultSrc: `${BASE_URL}/images/default-pic.jpg`,
        }
    },
    props: {
        src: { type: [String, Number], default: null },
        className: { type: String, default: () => 'image' },
    },
}
</script>
