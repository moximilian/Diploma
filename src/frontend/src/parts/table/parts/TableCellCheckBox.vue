<template>
    <TableCell>
        <input
            type="checkbox"
            class="custom-checkbox"
            :disabled="disabled"
            @change="click"
            :checked="isChecked"
            :title="title"
            :class="{disabled}"
        />
    </TableCell>
</template>
<script>
export default {
    props: {
        isCheckedDefault: { type: Boolean, default: () => false },
        disabled: { type: Boolean, default: () => false },
        title: { type: String, default: () => '' },
    },
    emits: ['clickCheckBox'],
    data() {
        return {
            isChecked: this.isCheckedDefault,
        }
    },
    methods: {
        click() {
            this.isChecked = !this.isChecked
            this.$emit('clickCheckBox', this.isChecked)
        },
    },
}
</script>
