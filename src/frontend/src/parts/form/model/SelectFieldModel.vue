<template>
    <SelectField
        v-bind="$props"
        type="search"
        :options="optionRows"
        :search="searchValue"
        :isLocalSearch="false"
        @changeValue="(...agr) => $emit('changeValue', ...agr)"
        @onOpened="opened"
        @search="searchCb"
    >
        <template #beforeInput>
            <slot name="beforeInput"></slot>
        </template>
    </SelectField>
</template>

<script>
import DropDownModelMixin from '../help/DropDownModelMixin'
export default {
    mixins: [DropDownModelMixin],
}
</script>
