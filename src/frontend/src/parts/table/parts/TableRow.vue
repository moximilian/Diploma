<template>
    <div class="table-base-row" @click="$emit('clickRow', row)" :class="{'clickable': isClickable}">
        <slot></slot>
    </div>
</template>
<script>
export default {
    props: {
        row: { type: Object, default: () => {} },
        isClickable: { type: Boolean, default: () => true },
    },
    emits: ['clickRow'],
}
</script>
