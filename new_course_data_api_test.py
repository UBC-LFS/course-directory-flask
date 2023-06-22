# Just a file to test code, does not effect actual application

import json

deptCourses = [
    {
        "@key": "260",
                "@title": "Agroecology I: Introduction to principles and techniques",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 260 001 2021W1"
    },
    {
        "@key": "210",
                "@title": "Vascular Plants",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "200",
                "@title": "Introduction to Soil Science",
                "@syllabusTerm": "2021SA",
                "@originalCourseName": "APBI 200 98A 2021SA"
    },
    {
        "@key": "244",
                "@title": "Atmospheric Environments",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "290",
                "@title": "Introductory Topics in Applied Biology",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 290 001 2021W1"
    },
    {
        "@key": "490-",
                "@title": "Advanced Topics in Applied Biology - TPCS APPL BIOLGY",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "314",
                "@title": "Animals and Society",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 314 001 2021W1"
    },
    {
        "@key": "327",
                "@title": "Introduction to Entomology",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "317",
                "@title": "Welfare and Ethics of using Animals in Science",
                "@syllabusTerm": "2021W2",
                "@originalCourseName": "APBI 317 002 2021W2"
    },
    {
        "@key": "318",
                "@title": "Applied Plant Breeding",
                "@syllabusTerm": "2022W1",
                "@originalCourseName": "APBI 318 001 2022W1"
    },
    {
        "@key": "316",
                "@title": "Equine Biology, Health and Welfare",
                "@syllabusTerm": "2022W2",
                "@originalCourseName": "APBI 316 001 2022W2"
    },
    {
        "@key": "319",
                "@title": "Aquaculture and the Environment",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "414",
                "@title": "Animals and Global Issues",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 414 001 2021W1"
    },
    {
        "@key": "328",
                "@title": "Weed Science",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 328 001 2021W1"
    },
    {
        "@key": "351",
                "@title": "Plant Physiology",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "426",
                "@title": "Plant-Microbe Interactions",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "402",
                "@title": "Sustainable Soil Management",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "412",
                "@title": "Belowground Ecosystems",
                "@syllabusTerm": "2021W2",
                "@originalCourseName": "APBI 412 001 2021W2"
    },
    {
        "@key": "428",
                "@title": "Integrated Pest Management",
                "@syllabusTerm": "2021SA",
                "@originalCourseName": "APBI 428 98A 2021SA"
    },
    {
        "@key": "444",
                "@title": "Agroforestry",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "342",
                "@title": "Soil Biology",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "419",
                "@title": "Fish Health",
                "@syllabusTerm": "2022W2",
                "@originalCourseName": "APBI 419 201 2022W2"
    },
    {
        "@key": "322",
                "@title": "Horticultural Techniques",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "497E",
                "@title": "Directed Studies - Directed Studies",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "410",
                "@title": "Applied Animal Health and Physiology",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 410 002 2021W1"
    },
    {
        "@key": "498",
                "@title": "Undergraduate Essay",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "315",
                "@title": "Animal Welfare and the Ethics of Animal Use",
                "@syllabusTerm": "2022W2",
                "@originalCourseName": "APBI 315 001 2022W2"
    },
    {
        "@key": "499",
                "@title": "Undergraduate Thesis",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "326",
                "@title": "Introductory Plant Pathology",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 326 001 2021W1"
    },
    {
        "@key": "440",
                "@title": "Plant Genomics",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "312",
                "@title": "Reproductive and Digestive Physiology",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 312 001 2021W1"
    },
    {
        "@key": "360",
                "@title": "Agroecology II: Application and analysis",
                "@syllabusTerm": "2021W2",
                "@originalCourseName": "APBI 360 001 2021W2"
    },
    {
        "@key": "311",
                "@title": "Comparative Cardiovascular, Respiratory and Osmoregulatory Physiology",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "496B",
                "@title": "Applied Animal Biology Practicum - Applied Animal Biology Practicum",
                "@syllabusTerm": "2021S1",
                "@originalCourseName": "APBI 496B 921 2021S1"
    },
    {
        "@key": "423",
                "@title": "Ecological Restoration",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "324",
                "@title": "Introduction to Seed Plant Taxonomy",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "497C",
                "@title": "Directed Studies - Directed Studies",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "460",
                "@title": "Agroecology III: Synthesis and evaluation",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 460 001 2021W1"
    },
    {
        "@key": "361",
                "@title": "Key Indicators of Agroecosystem Sustainability",
                "@syllabusTerm": "2021W2",
                "@originalCourseName": "APBI 361 199 2021W2"
    },
    {
        "@key": "418",
                "@title": "Intensive Fish Production",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "398",
                "@title": "Research Methods in Applied Biology",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 398 001 2021W1"
    },
    {
        "@key": "415",
                "@title": "Applied Animal Behaviour",
                "@syllabusTerm": "2021W2",
                "@originalCourseName": "APBI 415 001 2021W2"
    },
    {
        "@key": "495",
                "@title": "Human Wildlife Conflict",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "413",
                "@title": "Stress and Coping in Animals",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 413 001 2021W1"
    },
    {
        "@key": "427",
                "@title": "Insect Ecology",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "497B",
                "@title": "Directed Studies - Directed Studies",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "465",
                "@title": "Capstone in Sustainable Agriculture and Food Systems",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "416",
                "@title": "Compassionate Conservation",
                "@syllabusTerm": "2021W1",
                "@originalCourseName": "APBI 416 001 2021W1"
    },
    {
        "@key": "401",
                "@title": "Soil Processes",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "442",
                "@title": "Wine Grape and Berry Biology",
                "@syllabusTerm": "",
                "@originalCourseName": ""
    },
    {
        "@key": "265",
                "@title": "Sustainable Agriculture and Food Systems",
                "@syllabusTerm": "2021W2",
                "@originalCourseName": "APBI 265 001 2021W2"
    }
]

# Compares the courses and determines which one is higher


def courseOneIsHigher(courseOne, courseTwo):
    return (courseOne["@key"] > courseTwo["@key"])


# Sort courses in a department
for i in range(len(deptCourses)):
    for j in range(len(deptCourses)):
        if (j < (len(deptCourses) - 1)):
            if (courseOneIsHigher(deptCourses[j], deptCourses[j+1])):
                deptCourses[j], deptCourses[j + 1] = deptCourses[j+1], deptCourses[j]

with open("static/data/backedUpSessions/test.json", "w") as courseData:
    json.dump(deptCourses, courseData, indent=4)
print(deptCourses)
