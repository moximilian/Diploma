<template>
    <div class="filter-container">
        <div class="filters">
            <div class="filters-header">
                <div class="filter-title">Фильтры</div>
                <div class="filter-right"><a @click="resetForm">Очистить</a></div>
            </div>
            <div class="filter-content">
                <div
                    v-for="(filter, index) in displayFilters"
                    class="filter-item"
                    :key="filter.name"
                >
                    <component
                        :is="filter.display"
                        v-bind="filter.props"
                        :ref="`filter_${index}`"
                        @changeValue="
                            value => onChangeValue(value, filter.props.name, filter.condition)
                        "
                    >
                        <template #beforeInput>
                            <span class="field-title">{{ filter.props.title }}</span>
                        </template>
                    </component>
                    <div class="line" v-if="index > 0 && index < displayFilters.length - 1"></div>
                </div>
                <BaseBtn @click="applyFilters">Применить</BaseBtn>
            </div>
        </div>
    </div>
</template>
<style>
.filter-container {
    display: flex;
    margin-top: 32px;
}
.filters {
    display: flex;
    flex-direction: column;
    width: 320px;
}
.filters-header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}
.filter-title {
    font-weight: 800;
    font-size: 16px;
}
.filter-content {
    display: flex;
    flex-direction: column;
}
.filter-content .line {
    margin-top: 24px;
    width: 100%;
}
.filter-item {
    margin-bottom: 24px;
}

.filter-item input.field-input {
    width: calc(100% - 34px);
}

.filter-item .field-title {
    margin-bottom: 16px;
    font-weight: 800;
}
</style>
<script>
import displayRules from '@/core/displayRules'
export default {
    props: {
        filterName: { type: String, default: null },
    },
    emits: ['changeFilters'],
    data() {
        return {
            wheres: [],
            emptyValues: [null, undefined, ''],
        }
    },
    computed: {
        displayFilters() {
            return displayRules[`${this.filterName}Filter`]
        },
    },
    watch: {
        filterName: {
            handler() {
                this.setDefault()
            },
            immediate: true,
        },
    },
    methods: {
        onChangeValue(value, column, condition) {
            const newFilter = {
                value,
                column,
                condition,
            }
            if (this.emptyValues.includes(value))
                this.wheres.splice(
                    this.wheres.findIndex(where => where.column == column),
                    1
                )
            else {
                let whereExists = false
                this.wheres.reduce((wheres, where, index) => {
                    if (where.column === column) {
                        whereExists = true
                        wheres[index].value = value
                    }
                    return wheres
                }, this.wheres)
                !whereExists && this.wheres.push(newFilter)
            }
        },
        applyFilters() {
            this.$emit('changeFilters', this.wheres)
        },
        resetForm() {
            this.displayFilters.forEach((filter, index) => {
                ![null, undefined].includes(filter.props.value) &&
                    this.onChangeValue(filter.props.value, filter.props.name, filter.condition)
                this.$refs[`filter_${index}`].value = filter.props.value
            })
            this.wheres = []
            this.$emit('changeFilters', this.wheres)
        },
        setDefault() {
            this.displayFilters.forEach(filter => {
                const { value, name } = filter.props
                if (value) this.onChangeValue(value, name, filter.condition)
            })
            this.applyFilters()
        },
    },
    mounted() {
        this.setDefault()
    },
}
</script>
