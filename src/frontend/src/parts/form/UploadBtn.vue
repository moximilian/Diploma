<template>
    <div class="fieldFile">
        <slot name="beforeBtn" :file="file" :value="value" :focusFileInput="focusFileInput"></slot>
        <BaseBtn
            :outline="outline"
            :disabled="disabled"
            :showIcon="showIcon"
            @click="focusFileInput"
            >{{ text }}</BaseBtn
        >
        <input type="file" hidden :disabled="disabled" :accept="accept" @change="onChange" />
    </div>
</template>

<script>
export default {
    props: {
        accept: { type: String, default: null },
        disabled: { type: Boolean, default: null },
        requestPath: { type: String, default: null },
        showIcon: { type: Boolean, default: () => true },
        text: { type: [String, Boolean], default: () => false },
        value: { type: String, default: null },
        outline: { type: Boolean, default: () => false },
    },
    emits: ['onclick'],
    data() {
        return {
            waitConnect: false,
            status: null,
            fileInput: null,
            file: null,
        }
    },
    methods: {
        focusFileInput() {
            if (this.disabled) return
            this.fileInput.click()
        },
        onChange() {
            if (this.waitConnect) return
            this.waitConnect = true
            this.status = null
            this.file = this.fileInput?.files?.[0]
            if (!this.file) return

            const reader = new FileReader()
            reader.onload = (e) => {
                const base64String = e.target.result
                base64String && this.$emit('onclick', base64String, this.file.name)
            }
            reader.readAsDataURL(this.file)
             
        },
    },
    mounted() {
        this.fileInput = this.$el.querySelector('input[type="file"]')
    },
}
</script>
