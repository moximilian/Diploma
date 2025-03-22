<template>
    <div class="page-container">
        <div class="page user">
            <div class="page-header-wrapper">
                <div class="page-title">{{ title }}</div>
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
}
</script>
