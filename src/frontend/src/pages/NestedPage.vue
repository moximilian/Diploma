<template>
    <div class="page-container">
        <div class="page user">
            <div class="page-header-wrapper">
                <div class="page-title">{{ viewTitle }}</div>
                <div class="page-right">
                    <slot name="page-header-right"></slot>
                </div>
            </div>
            <slot name="page-content"></slot>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        title: { type: [String, Boolean], default: () => '' },
    },
    computed: {
        viewTitle() {
            if (this.title.length > 64) {
                const toDelete = this.title.substring(45, this.title.length)
                return this.title.replace(toDelete, '') + '...'
            }
            return this.title
        },
    },
}
</script>
