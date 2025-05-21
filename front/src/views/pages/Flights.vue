<script setup>
import { FilterMatchMode } from '@primevue/core/api';
import { useToast } from 'primevue/usetoast';
import { onMounted, ref } from 'vue';
import api from '@/axios';
import router from '@/router';

function fetchFlights() {
    api.get('/flights/').then((response) => {
        flights.value = response.data.map((flight) => {
            // Remove seconds from time fields
            flight.departure_time = removeSeconds(flight.departure_time);
            flight.arrival_time = removeSeconds(flight.arrival_time);
            flight.flight_duration = removeSeconds(flight.flight_duration);
            flight.se_duration = removeSeconds(flight.se_duration);
            flight.me_duration = removeSeconds(flight.me_duration);
            flight.multi_pilot_duration = removeSeconds(flight.multi_pilot_duration);
            flight.night_duration = removeSeconds(flight.night_duration);
            flight.ifr_duration = removeSeconds(flight.ifr_duration);
            flight.pilot_in_command_duration = removeSeconds(flight.pilot_in_command_duration);
            flight.copilot_duration = removeSeconds(flight.copilot_duration);
            flight.dual_duration = removeSeconds(flight.dual_duration);
            flight.instructor_duration = removeSeconds(flight.instructor_duration);
            flight.simulator_duration = removeSeconds(flight.simulator_duration);
            return flight;
        });
    });
}
// Call the function in onMounted
onMounted(() => {
    fetchFlights();
    api.get('/planes/').then((response) => (dropdownPlanes.value = response.data)); // Fetch planes for dropdown
    api.get('/people/?is_pilot=true').then((response) => (dropdownPilots.value = response.data)); // Fetch pilots for dropdown
    api.get('/people/').then((response) => (dropdownPassengers.value = response.data)); // Fetch passengers for dropdown
});


const toast = useToast();
const dt = ref();
const flights = ref();
const flightDialog = ref(false);
const deleteFlightDialog = ref(false);
const deleteflightsDialog = ref(false);
const flight = ref({});
const dropdownPlanes = ref([]); // Ref to store planes for the dropdown
const dropdownPilots = ref([]); // Ref to store pilots for the dropdown
const dropdownPassengers = ref([]); // Ref to store passengers for the dropdown
const selectedflights = ref();
const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS }
});
const submitted = ref(false);

function removeSeconds(time) {
    if (typeof time === 'string' && time.includes(':')) {
        const parts = time.split(':');
        return parts.length > 2 ? `${parts[0]}:${parts[1]}` : time; // Keep only hours and minutes
    }
    return time;
}

function openNew() {
    flight.value = {}; // Clear the flight object
    router.push({ name: 'flight', params: { id: 'new' } }); // Redirect to the flightForm page with a new id
}

function hideDialog() {
    flightDialog.value = false;
    submitted.value = false;
}

function formatDuration(value) {
        if (!value) {
            return "00:00:00";
        } else {
            // If value is a Date object, format it to HH:MM:SS
            if (value instanceof Date) {
                value = value.toTimeString().split(' ')[0]
            }
        }
        console.log(value)
        return value
    }

function saveflight() {
    submitted.value = true;

    // Helper function to format duration values


    // Format all duration fields
    console.log(flight.value)
    flight.value.date = (flight.value.date instanceof Date)
    ? flight.value.date.toISOString().split('T')[0]
    : new Date(flight.value.date).toISOString().split('T')[0];
    flight.value.departure_time = formatDuration(flight.value.departure_time);
    flight.value.arrival_time = formatDuration(flight.value.arrival_time);
    flight.value.flight_duration = formatDuration(flight.value.flight_duration);
    flight.value.se_duration = formatDuration(flight.value.se_duration);
    flight.value.me_duration = formatDuration(flight.value.me_duration);
    flight.value.multi_pilot_duration = formatDuration(flight.value.multi_pilot_duration);
    flight.value.night_duration = formatDuration(flight.value.night_duration);
    flight.value.ifr_duration = formatDuration(flight.value.ifr_duration);
    flight.value.pilot_in_command_duration = formatDuration(flight.value.pilot_in_command_duration);
    flight.value.copilot_duration = formatDuration(flight.value.copilot_duration);
    flight.value.dual_duration = formatDuration(flight.value.dual_duration);
    flight.value.instructor_duration = formatDuration(flight.value.instructor_duration);
    flight.value.simulator_duration = formatDuration(flight.value.simulator_duration);

    flight.value.pilot_in_command = flight.value.pilot_in_command.id;
    flight.value.plane = flight.value.plane.id;
    flight.value.passengers = flight.value.passengers.map((passenger) => passenger.id); // Map passengers to their IDs

    if (flight.value.id) {
        const index = findIndexById(flight.value.id);
        flights.value[index] = { ...flights.value[index], ...flight.value };
        api.put(`/flights/${flight.value.id}/`, flight.value)
            .then(() => {
                flights.value[index] = flight.value;
                flightDialog.value = false;
                flight.value = {};
                toast.add({ severity: 'success', summary: 'Successful', detail: 'FlightUpdated', life: 3000 });
                fetchFlights()
            })
            .catch((error) => {
                console.error(error);
                toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to update flight', life: 3000 });
            });
    } else {
        if (
            true
        ) {
            api.post('/flights/', flight.value)
                .then((response) => {
                    flights.value.push(response.data); // Add the newly created flight to the list
                    flightDialog.value = false;
                    flight.value = {};
                    toast.add({ severity: 'success', summary: 'Successful', detail: 'FlightCreated', life: 3000 });
                })
                .catch((error) => {
                    console.error(error);
                    toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to create flight', life: 3000 });
                });
        }
    }
}

function editFlight(prod) {
    router.push({ name: 'flight', params: { id: prod.id } });
    //flight.value = { ...prod };
    // // Ensure flight.plane is the full object from dropdown
    //const fullPlane = dropdownPlanes.value.find(
    //    (plane) => plane.id === prod.plane?.id || plane.id === prod.plane
    //);
    //if (fullPlane) {
    //    flight.value.plane = fullPlane;
    //}
//
    //// Same for pilot
    //const fullPilot = dropdownPilots.value.find(
    //    (pilot) => pilot.id === prod.pilot_in_command?.id || pilot.id === prod.pilot_in_command
    //);
    //if (fullPilot) {
    //    flight.value.pilot_in_command = fullPilot;
    //}
//
    //const fullPassengers = prod.passengers.map((passenger) => {
    //    return dropdownPassengers.value.find(
    //        (p) => p.id === passenger.id || p.id === passenger
    //    );
    //});
    //if (fullPassengers) {
    //    flight.value.passengers = fullPassengers;
    //}
//
    ////flight.value.plane = dropdownPlanes.value.find(plane => plane.id === prod.plane?.id || plane.id === prod.plane);
    ////flight.value.pilot_in_command = dropdownPilots.value.find(pilot => pilot.id === prod.pilot_in_command?.id || pilot.id === prod.pilot_in_command);
    //flightDialog.value = true;
}

function confirmDeleteFlight(prod) {
    flight.value = prod;
    deleteFlightDialog.value = true;
}

function deleteflight() {
    api.delete(`/flights/${flight.value.id}/`)
        .then(() => {
            flights.value = flights.value.filter((val) => val.id !== flight.value.id);
            deleteFlightDialog.value = false;
            flight.value = {};
            toast.add({ severity: 'success', summary: 'Successful', detail: 'FlightDeleted', life: 3000 });
        })
        .catch((error) => {
            console.error(error);
            toast.add({ severity: 'error', summary: 'Error', detail: 'Failed to delete flight', life: 3000 });
        });
}
function compute_price(flight) {
    if (typeof flight.price === 'number' && flight.price > 0) {
        flight.price =  flight.price; // Return the existing price if already calculated
    }
    else if (flight.flight_duration && flight.plane && flight.plane.hour_price) {
        const timeParts = formatDuration(flight.flight_duration).split(':');
        const timeHoursFloat = parseInt(timeParts[0], 10) + parseInt(timeParts[1], 10) / 60;
        console.log("Time in hours:", timeHoursFloat);
        console.log("Plane price per hour:", flight.plane.hour_price);
        if (flight.pilot_in_command.is_instructor) {
            flight.price = (flight.plane.hour_price * timeHoursFloat + flight.plane.instructor_hour_price * timeHoursFloat).toFixed(2); // Increase price by 50% for instructor
        } else {
            flight.price = (flight.plane.hour_price * timeHoursFloat).toFixed(2);
        }
        console.log("Computed price:", flight.price);
    } else {
        flight.price = 0; // Default to 0 if required data is missing
    }
    console.log(flight.price)
}

function findIndexById(id) {
    let index = -1;
    for (let i = 0; i < flights.value.length; i++) {
        if (flights.value[i].id === id) {
            index = i;
            break;
        }
    }

    return index;
}

function exportCSV() {
    dt.value.exportCSV();
}

function confirmDeleteSelected() {
    deleteflightsDialog.value = true;
}

function deleteSelectedflights() {
    flights.value = flights.value.filter((val) => !selectedflights.value.includes(val));
    deleteflightsDialog.value = false;
    selectedflights.value = null;
    toast.add({ severity: 'success', summary: 'Successful', detail: 'flights Deleted', life: 3000 });
}
</script>

<template>
    <div>
        <div class="card">
            <Toolbar class="mb-6">
                <template #start>
                    <Button label="New" icon="pi pi-plus" severity="secondary" class="mr-2" @click="openNew" />
                    <Button label="Delete" icon="pi pi-trash" severity="secondary" @click="confirmDeleteSelected" :disabled="!selectedflights || !selectedflights.length" />
                </template>

                <template #end>
                    <Button label="Export" icon="pi pi-upload" severity="secondary" @click="exportCSV($event)" />
                </template>
            </Toolbar>

            <DataTable
                ref="dt"
                v-model:selection="selectedflights"
                :value="flights"
                dataKey="id"
                :paginator="true"
                :rows="10"
                :filters="filters"
                paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
                :rowsPerPageOptions="[5, 10, 25]"
                currentPageReportTemplate="Showing {first} to {last} of {totalRecords} flights"
            >
                <template #header>
                    <div class="flex flex-wrap gap-2 items-center justify-between">
                        <h4 class="m-0">Manage flights</h4>
                        <IconField>
                            <InputIcon>
                                <i class="pi pi-search" />
                            </InputIcon>
                            <InputText v-model="filters['global'].value" placeholder="Search..." />
                        </IconField>
                    </div>
                </template>

                <Column selectionMode="multiple" style="width: 3rem" :exportable="false"></Column>
                <Column field="id" header="Id" sortable style="min-width: 4rem"></Column>
                <Column field="date" header="Date" sortable style="min-width: 8rem"></Column>
                <Column field="departure_airport" header="Departure Airport" sortable style="min-width: 6rem"></Column>
                <Column field="departure_time" header="Departure Time" sortable style="min-width: 6rem"></Column>
                <Column field="arrival_airport" header="Arrival Airport" sortable style="min-width: 6rem"></Column>
                <Column field="arrival_time" header="Arrival Time" sortable style="min-width: 6rem"></Column>
                <Column field="plane.model" header="Plane" sortable style="min-width: 10rem"></Column>
                <Column field="plane.registration_number" header="Registration" sortable style="min-width: 8rem"></Column>
                <Column field="se_duration" header="Single Engine Duration" sortable style="min-width: 6rem"></Column>
                <Column field="me_duration" header="Multi Engine Duration" sortable style="min-width: 6rem"></Column>
                <Column field="multi_pilot_duration" header="Multi Pilot Duration" sortable style="min-width: 6rem"></Column>
                <Column field="flight_duration" header="Flight Duration" sortable style="min-width: 6rem"></Column>
                <Column field="pilot_in_command.last_name" header="Pilot" sortable style="min-width: 12rem"></Column>
                <Column field="landing_day_num" header="Landing Day" sortable style="min-width: 6rem"></Column>
                <Column field="landing_night_num" header="Landing Night" sortable style="min-width: 6rem"></Column>
                <Column field="ifr_apch_num" header="IFR Approach" sortable style="min-width: 6rem"></Column>
                <Column field="night_duration" header="Night Duration" sortable style="min-width: 6rem"></Column>
                <Column field="ifr_duration" header="IFR Duration" sortable style="min-width: 6rem"></Column>
                <Column field="pilot_in_command_duration" header="Pilot in Command Duration" sortable style="min-width: 6rem"></Column>
                <Column field="copilot_duration" header="Co-Pilot Duration" sortable style="min-width: 6rem"></Column>
                <Column field="dual_duration" header="Dual Duration" sortable style="min-width: 6rem"></Column>
                <Column field="instructor_duration" header="Instructor Duration" sortable style="min-width: 6rem"></Column>
                <Column field="simulator_date" header="Simulator Date" sortable style="min-width: 6rem"></Column>
                <Column field="simulator_type" header="Simulator Type" sortable style="min-width: 12rem"></Column>
                <Column field="simulator_duration" header="Simulator Duration" sortable style="min-width: 6rem"></Column>
                <Column field="comments" header="Comments" sortable style="min-width: 12rem"></Column>
                <Column field="passengers" header="Passengers" sortable style="min-width: 20rem">
                    <template #body="slotProps">
                        <div class="flex flex-wrap gap-2">
                            <Chip 
                                v-for="passenger in slotProps.data.passengers" 
                                :key="passenger.id" 
                                :label="`${passenger.first_name} ${passenger.last_name}`" 
                                class="mr-2 mb-2" 
                            />
                        </div>
                    </template>
                </Column>
                <Column field="price" header="Price (€)" sortable style="min-width: 6rem"></Column>
                <Column :exportable="false" style="min-width: 12rem">
                    <template #body="slotProps">
                        <Button icon="pi pi-pencil" outlined rounded class="mr-2" @click="editFlight(slotProps.data)" />
                        <Button icon="pi pi-trash" outlined rounded severity="danger" @click="confirmDeleteFlight(slotProps.data)" />
                    </template>
                </Column>
            </DataTable>
        </div>

        <Dialog v-model:visible="flightDialog" :style="{ width: '450px' }" header="flight Details" :modal="true">
            <div class="flex flex-col gap-6">
                <img v-if="flight.image" :src="`https://primefaces.org/cdn/primevue/images/flight/${flight.image}`" :alt="flight.image" class="block m-auto pb-4" />
                <div>
                    <label for="date" class="block font-bold mb-3">Date</label>
                    <DatePicker 
                        id="date" 
                        :showIcon="true" 
                        :showButtonBar="true" 
                        v-model="flight.date" 
                        :placeholder="'Select Date'" 
                        required="true" 
                        :invalid="submitted && !flight.date" 
                    />
                </div>
                <div>
                    <label for="departure_airport" class="block font-bold mb-3">Departure Airport</label>
                    <InputText id="departure_airport" v-model.trim="flight.departure_airport" required="true" autofocus :invalid="submitted && !flight.departure_airport" fluid />
                </div>
                <div>
                    <label for="departure_time" class="block font-bold mb-3">Departure Time</label>
                    <DatePicker id="departure_time" v-model="flight.departure_time" timeOnly fluid />
                </div>
                <div>
                    <label for="arrival_airport" class="block font-bold mb-3">Arrival Airport</label>
                    <InputText id="arrival_airport" v-model.trim="flight.arrival_airport" required="true" autofocus :invalid="submitted && !flight.arrival_airport" fluid />
                </div>
                <div>
                    <label for="arrival_time" class="block font-bold mb-3">Arrival Time</label>
                    <DatePicker id="arrival_time" v-model="flight.arrival_time" timeOnly fluid />
                </div>
                <div>
                    <label for="plane" class="block font-bold mb-3">Plane</label>
                    <Select v-model="flight.plane" :options="dropdownPlanes" optionLabel="registration_number" placeholder="Select" 
                    @update:model-value="(value) => {
                        update_price(flight)
                    }"/>
                </div>
                <div>
                    <label for="flight_duration" class="block font-bold mb-3">Flight Duration</label>
                    <DatePicker 
                        id="flight_duration" 
                        v-model="flight.flight_duration" 
                        timeOnly 
                        fluid 
                        @update:model-value="(value) => {
                            flight.flight_duration = value;
                            if (flight.plane && flight.plane.single_engine === true) {
                                flight.se_duration = value;
                            }
                            if (flight.plane && flight.plane.single_engine === false) {
                                flight.me_duration = value;
                            }
                            if (flight.plane && flight.plane.single_pilot === false) {
                                flight.multi_pilot_duration = value;
                            }
                            compute_price(flight)
                        }"
                    />
                </div>
                <div>
                    <label for="se_duration" class="block font-bold mb-3">Single Engine Duration</label>
                    <DatePicker 
                        id="se_duration" 
                        v-model="flight.se_duration" 
                        timeOnly 
                        fluid 
                        :disabled="flight.plane && flight.plane.single_engine" 
                    />
                </div>
                <div>
                    <label for="me_duration" class="block font-bold mb-3">Multi Engine Duration</label>
                    <DatePicker 
                        id="me_duration" 
                        v-model="flight.me_duration" 
                        timeOnly 
                        fluid 
                        :disabled="flight.plane && flight.plane.single_engine"
                    />
                </div>
                <div>
                    <label for="multi_pilot_duration" class="block font-bold mb-3">Multi Pilot Duration</label>
                    <DatePicker
                        id="multi_pilot_duration"
                        v-model="flight.multi_pilot_duration"
                        timeOnly
                        fluid
                        />
                </div>
                <div>
                    <label for="pilot_in_command" class="block font-bold mb-3">Pilot in Command</label>
                    <Select v-model="flight.pilot_in_command" :options="dropdownPilots" optionLabel="last_name" placeholder="Select" 
                    @update:model-value="(value) => {
                            flight.pilot_in_command = value;
                            if (flight.pilot_in_command.is_main_pilot === true) {
                                flight.pilot_in_command_duration = flight.flight_duration;
                            }
                            if (flight.pilot_in_command.is_main_pilot === false) {
                                flight.dual_duration = flight.flight_duration;
                            }
                        }"/>
                </div>
                <div>
                    <label for="landing_day_num" class="block font-bold mb-3">Landing Day</label>
                    <InputNumber id="landing_day_num" v-model.trim="flight.landing_day_num" required="true" autofocus fluid />
                </div>
                <div>
                    <label for="landing_night_num" class="block font-bold mb-3">Landing Night</label>
                    <InputNumber id="landing_night_num" v-model.trim="flight.landing_night_num" required="true" autofocus fluid />
                </div>
                <div>
                    <label for="ifr_apch_num" class="block font-bold mb-3">IFR Approach</label>
                    <InputNumber id="ifr_apch_num" v-model.trim="flight.ifr_apch_num" required="true" autofocus fluid />
                </div>
                <div>
                    <label for="night_duration" class="block font-bold mb-3">Night Duration</label>
                    <DatePicker id="night_duration" v-model="flight.night_duration" timeOnly fluid />
                </div>
                <div>
                    <label for="ifr_duration" class="block font-bold mb-3">IFR Duration</label>
                    <DatePicker id="ifr_duration" v-model="flight.ifr_duration" timeOnly fluid />
                </div>
                <div>
                    <label for="pilot_in_command_duration" class="block font-bold mb-3">Pilot in Command Duration</label>
                    <DatePicker id="pilot_in_command_duration" v-model="flight.pilot_in_command_duration" timeOnly fluid />
                </div>
                <div>
                    <label for="copilot_duration" class="block font-bold mb-3">Co-Pilot Duration</label>
                    <DatePicker id="copilot_duration" v-model="flight.copilot_duration" timeOnly fluid />
                </div>
                <div>
                    <label for="dual_duration" class="block font-bold mb-3">Dual Duration</label>
                    <DatePicker id="dual_duration" v-model="flight.dual_duration" timeOnly fluid />
                </div>
                <div>
                    <label for="instructor_duration" class="block font-bold mb-3">Instructor Duration</label>
                    <DatePicker id="instructor_duration" v-model="flight.instructor_duration" timeOnly fluid />
                </div>
                <div>
                    <label for="passengers" class="block font-bold mb-3">Passengers</label>
                    <MultiSelect v-model="flight.passengers" :options="dropdownPassengers" optionLabel="name" placeholder="Select Passengers" :filter="true">
                    <template #value="slotProps">
                        <div class="inline-flex items-center py-1 px-2 bg-primary text-primary-contrast rounded-border mr-2" v-for="option of slotProps.value" :key="option.code">
                            <div>{{ option.first_name }} {{ option.last_name }}</div>
                        </div>
                        <template v-if="!slotProps.value || slotProps.value.length === 0">
                            <div class="p-1">Select Passengers</div>
                        </template>
                    </template>
                    <template #option="slotProps">
                        <div class="flex items-center">
                            <div>{{ slotProps.option.first_name }} {{ slotProps.option.last_name }}</div>
                        </div>
                    </template>
                </MultiSelect>
                </div>
                <div>
                    <label for="price" class="block font-bold mb-3">Price</label>
                    <InputText id="price" v-model.trim="flight.price" required="true" autofocus :invalid="submitted && !flight.price" fluid />
                </div>

            </div>

            <template #footer>
                <Button label="Cancel" icon="pi pi-times" text @click="hideDialog" />
                <Button label="Save" icon="pi pi-check" @click="saveflight" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteFlightDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="flight"
                    >Are you sure you want to delete <b>{{ flight.first_name }} {{ flight.last_name }}</b
                    >?</span
                >
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteflightDialog = false" />
                <Button label="Yes" icon="pi pi-check" @click="deleteflight" />
            </template>
        </Dialog>

        <Dialog v-model:visible="deleteflightsDialog" :style="{ width: '450px' }" header="Confirm" :modal="true">
            <div class="flex items-center gap-4">
                <i class="pi pi-exclamation-triangle !text-3xl" />
                <span v-if="flight">Are you sure you want to delete the selected flights?</span>
            </div>
            <template #footer>
                <Button label="No" icon="pi pi-times" text @click="deleteflightsDialog = false" />
                <Button label="Yes" icon="pi pi-check" text @click="deleteSelectedflights" />
            </template>
        </Dialog>
    </div>
</template>
