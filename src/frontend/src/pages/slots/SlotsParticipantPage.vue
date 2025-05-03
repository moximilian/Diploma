<template>
    <div>
        <TableView
            ref="table"
            :keys="[...keys, ...checkBoxKeys, ...customKeysForTable]"
            displayName="slotParticipants"
            :defaultFilters="defaultFilters"
            :filters="defaultFilters.filters"
            orderByLocal="datetime"
            :isClickable="false"
            @loaded="getCustomKeysForTable"
            @onCustomKeyDelete="deleteCustomKey"
        >
            <template #table-cell="{ row, keyObj }">
                <TableCellCheckBox
                    v-if="checkBoxKeys.includes(keyObj)"
                    :isCheckedDefault="row[keyObj.name]"
                    @clickCheckBox="
                        async isChecked => await onCheckedChange(isChecked, keyObj.name, row)
                    "
                />
                <div v-if="keyObj?.isCustom === true">
                    <InputField
                        :value="row.custom?.[keyObj.name]"
                        :ref="`input${keyObj.name}${row.id}`"
                        @changeValue="value => setValueForCustomField(keyObj.name, value, row)"
                    />
                </div>
            </template>
            <template #custom-title-key="{ rows }">
                <div class="table-cell">
                    <div class="flex-container-column">
                        <div class="flex-container-row" v-if="!isShowCustomInput">
                            Добавить новую характеристику
                            <BaseBtn class="small" :outline="true" @click="toggleCustomInput"
                                >+</BaseBtn
                            >
                        </div>
                        <div class="flex-container-row" v-if="isShowCustomInput">
                            <InputField
                                placeholder="Например, ДЗ"
                                @changeValue="setNewCustomTitle"
                            />
                            <BaseBtn
                                class="small"
                                :outline="true"
                                :disabled="!newCustomKey"
                                @click="() => addNewCustomTitle(rows)"
                                >+</BaseBtn
                            >
                        </div>
                    </div>
                </div>
            </template>
            <template #last-item>
                <TableCell />
            </template>
        </TableView>
    </div>
</template>
<script>
import ParticipantsMixin from '../_help/ParticipantsMixin'
export default {
    mixins: [ParticipantsMixin],
    computed: {
        defaultFilters() {
            return {
                filters: {
                    wheres: [
                        {
                            column: 'slot_id',
                            value: this.slotId,
                        },
                    ],
                },
            }
        },
    },
    methods: {
        async updateRow(entity) {
            await this.$api.slotParticipants.update(entity)
            this.$refs.table.load()
        },
    },
    created() {
        this.slotId = this.$route.params.id
    },
}
</script>
