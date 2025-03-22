<template>
    <div class="table-base-row" @click="$emit('clickRow', row)">
        <slot></slot>
    </div>
</template>
<script>
export default {
    props: {
        row: {type: Object, default: () => {}}
    },
    emits: ['clickRow'],
}
</script>
