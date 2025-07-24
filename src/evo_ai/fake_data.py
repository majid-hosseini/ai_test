"""
Fake API responses for testing the Evo AI Agent.
This module contains realistic geological data for testing agent functionality.
"""

from typing import Any, Dict, List

# Fake API response for get_list_of_objects (latest versions only)
FAKE_OBJECTS_LIST: List[Dict[str, Any]] = [
    {
        "id": "obj_001",
        "name": "thalanga_local_drillholes_dt",
        "object_type": "downhole-collection",
        "created_date": "2024-01-15T10:30:00Z",
        "created_by": "john.smith@seequent.com",
        "description": "Downhole collection for Thalanga local drilling data",
        "version": "latest",
        "assays": ["gold", "silver", "copper", "zinc"]
    },
    {
        "id": "obj_002", 
        "name": "thalanga_local_drillholes_e_sm",
        "object_type": "downhole-collection",
        "created_date": "2024-01-20T14:45:00Z",
        "created_by": "jane.doe@seequent.com",
        "description": "Enhanced downhole collection with detailed assays",
        "version": "latest",
        "assays": ["gold", "silver", "copper", "lead", "zinc", "iron"]
    },
    {
        "id": "obj_003",
        "name": "surface_geology_pointset",
        "object_type": "pointset",
        "created_date": "2024-01-25T09:15:00Z",
        "created_by": "mike.johnson@seequent.com",
        "description": "Surface geology sampling points",
        "version": "latest",
        "attributes": ["formation", "rock_type", "alteration"]
    },
    {
        "id": "obj_004",
        "name": "mineral_occurrences_pointset",
        "object_type": "pointset",
        "created_date": "2024-02-01T11:20:00Z",
        "created_by": "sarah.wilson@seequent.com",
        "description": "Mineral occurrence locations and characteristics",
        "version": "latest",
        "attributes": ["mineral_type", "grade", "tonnage"]
    },
    {
        "id": "obj_005",
        "name": "exploration_drillholes_main",
        "object_type": "downhole-collection",
        "created_date": "2024-02-10T16:00:00Z",
        "created_by": "david.brown@seequent.com",
        "description": "Main exploration drilling program results",
        "version": "latest",
        "assays": ["gold", "silver", "copper", "molybdenum", "uranium"]
    },
    {
        "id": "obj_006",
        "name": "structural_measurements_pointset",
        "object_type": "pointset",
        "created_date": "2024-02-15T13:30:00Z",
        "created_by": "emma.taylor@seequent.com",
        "description": "Structural geology measurements and orientations",
        "version": "latest",
        "attributes": ["dip", "strike", "structure_type", "confidence"]
    }
]


# Fake API response for get_list_of_objects_all_versions (includes version history)
FAKE_OBJECTS_ALL_VERSIONS: List[Dict[str, Any]] = [
    {
        "id": "obj_001",
        "name": "thalanga_local_drillholes_dt",
        "object_type": "downhole-collection",
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-01-10T08:00:00Z",
                "created_by": "john.smith@seequent.com",
                "description": "Initial version"
            },
            {
                "version_id": "v2",
                "created_date": "2024-01-15T10:30:00Z",
                "created_by": "john.smith@seequent.com",
                "description": "Updated with additional assays"
            }
        ],
        "total_versions": 2,
        "latest_version": "v2"
    },
    {
        "id": "obj_002",
        "name": "thalanga_local_drillholes_e_sm",
        "object_type": "downhole-collection",
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-01-18T12:00:00Z",
                "created_by": "jane.doe@seequent.com",
                "description": "Initial enhanced version"
            },
            {
                "version_id": "v2",
                "created_date": "2024-01-20T14:45:00Z",
                "created_by": "jane.doe@seequent.com",
                "description": "Added lead and iron assays"
            },
            {
                "version_id": "v3",
                "created_date": "2024-01-25T16:15:00Z",
                "created_by": "jane.doe@seequent.com",
                "description": "Quality control and validation updates"
            }
        ],
        "total_versions": 3,
        "latest_version": "v3"
    },
    {
        "id": "obj_003",
        "name": "surface_geology_pointset",
        "object_type": "pointset",
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-01-25T09:15:00Z",
                "created_by": "mike.johnson@seequent.com",
                "description": "Initial surface geology data"
            }
        ],
        "total_versions": 1,
        "latest_version": "v1"
    },
    {
        "id": "obj_004",
        "name": "mineral_occurrences_pointset",
        "object_type": "pointset",
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-02-01T11:20:00Z",
                "created_by": "sarah.wilson@seequent.com",
                "description": "Initial mineral occurrences"
            },
            {
                "version_id": "v2",
                "created_date": "2024-02-05T15:30:00Z",
                "created_by": "sarah.wilson@seequent.com",
                "description": "Added tonnage estimates"
            }
        ],
        "total_versions": 2,
        "latest_version": "v2"
    }
]


# Fake detailed object information database for get_objects_info
FAKE_OBJECTS_DATABASE: Dict[str, Dict[str, Any]] = {
    "thalanga_local_drillholes_dt": {
        "id": "obj_001",
        "name": "thalanga_local_drillholes_dt",
        "object_type": "downhole-collection",
        "description": "Downhole collection for Thalanga local drilling data",
        "created_date": "2024-01-15T10:30:00Z",
        "created_by": "john.smith@seequent.com",
        "bounding_box": {
            "min_x": 345000.0,
            "max_x": 347500.0,
            "min_y": 6785000.0,
            "max_y": 6787500.0,
            "min_z": -500.0,
            "max_z": 50.0
        },
        "dimensions": {
            "length": 2500.0,  # max_x - min_x
            "width": 2500.0,   # max_y - min_y
            "depth": 550.0     # max_z - min_z
        },
        "assays": [
            {
                "element": "gold",
                "min_value": 0.001,
                "max_value": 15.8,
                "average_value": 2.3,
                "unit": "g/t"
            },
            {
                "element": "silver",
                "min_value": 0.5,
                "max_value": 145.2,
                "average_value": 18.7,
                "unit": "g/t"
            },
            {
                "element": "copper",
                "min_value": 0.01,
                "max_value": 3.2,
                "average_value": 0.8,
                "unit": "%"
            },
            {
                "element": "zinc",
                "min_value": 0.05,
                "max_value": 8.9,
                "average_value": 2.1,
                "unit": "%"
            }
        ],
        "collections": {
            "holes": 45,
            "intervals": 1250,
            "total_length": 12500.0
        }
    },
    "thalanga_local_drillholes_e_sm": {
        "id": "obj_002",
        "name": "thalanga_local_drillholes_e_sm",
        "object_type": "downhole-collection",
        "description": "Enhanced downhole collection with detailed assays",
        "created_date": "2024-01-20T14:45:00Z",
        "created_by": "jane.doe@seequent.com",
        "bounding_box": {
            "min_x": 344500.0,
            "max_x": 348000.0,
            "min_y": 6784500.0,
            "max_y": 6788000.0,
            "min_z": -600.0,
            "max_z": 75.0
        },
        "dimensions": {
            "length": 3500.0,  # max_x - min_x
            "width": 3500.0,   # max_y - min_y
            "depth": 675.0     # max_z - min_z
        },
        "assays": [
            {
                "element": "gold",
                "min_value": 0.005,
                "max_value": 22.4,
                "average_value": 3.1,
                "unit": "g/t"
            },
            {
                "element": "silver",
                "min_value": 0.2,
                "max_value": 189.6,
                "average_value": 25.3,
                "unit": "g/t"
            },
            {
                "element": "copper",
                "min_value": 0.008,
                "max_value": 4.1,
                "average_value": 1.2,
                "unit": "%"
            },
            {
                "element": "lead",
                "min_value": 0.02,
                "max_value": 6.7,
                "average_value": 1.8,
                "unit": "%"
            },
            {
                "element": "zinc",
                "min_value": 0.03,
                "max_value": 12.3,
                "average_value": 3.4,
                "unit": "%"
            },
            {
                "element": "iron",
                "min_value": 2.1,
                "max_value": 35.8,
                "average_value": 18.2,
                "unit": "%"
            }
        ],
        "collections": {
            "holes": 62,
            "intervals": 1845,
            "total_length": 18750.0
        }
    },
    "surface_geology_pointset": {
        "id": "obj_003",
        "name": "surface_geology_pointset",
        "object_type": "pointset",
        "description": "Surface geology sampling points",
        "created_date": "2024-01-25T09:15:00Z",
        "created_by": "mike.johnson@seequent.com",
        "bounding_box": {
            "min_x": 344000.0,
            "max_x": 349000.0,
            "min_y": 6784000.0,
            "max_y": 6789000.0,
            "min_z": -50.0,
            "max_z": 250.0
        },
        "dimensions": {
            "length": 5000.0,  # max_x - min_x
            "width": 5000.0,   # max_y - min_y
            "depth": 300.0     # max_z - min_z
        },
        "attributes": [
            {
                "name": "formation",
                "type": "categorical",
                "values": ["Thalanga Formation", "Cambrian Volcanics", "Ordovician Sediments"],
                "dominant_value": "Thalanga Formation"
            },
            {
                "name": "rock_type",
                "type": "categorical",
                "values": ["Basalt", "Rhyolite", "Sedimentary", "Volcanic Breccia"],
                "dominant_value": "Basalt"
            },
            {
                "name": "alteration",
                "type": "categorical",
                "values": ["Fresh", "Weak", "Moderate", "Strong", "Intense"],
                "dominant_value": "Moderate"
            }
        ],
        "collections": {
            "points": 134,
            "area_coverage": 25.0  # km²
        }
    },
    "mineral_occurrences_pointset": {
        "id": "obj_004",
        "name": "mineral_occurrences_pointset",
        "object_type": "pointset",
        "description": "Mineral occurrence locations and characteristics",
        "created_date": "2024-02-01T11:20:00Z",
        "created_by": "sarah.wilson@seequent.com",
        "bounding_box": {
            "min_x": 340000.0,
            "max_x": 355000.0,
            "min_y": 6780000.0,
            "max_y": 6795000.0,
            "min_z": -100.0,
            "max_z": 400.0
        },
        "dimensions": {
            "length": 15000.0,  # max_x - min_x
            "width": 15000.0,   # max_y - min_y
            "depth": 500.0      # max_z - min_z
        },
        "attributes": [
            {
                "name": "mineral_type",
                "type": "categorical",
                "values": ["Pyrite", "Chalcopyrite", "Galena", "Sphalerite", "Magnetite"],
                "dominant_value": "Pyrite"
            },
            {
                "name": "grade",
                "type": "numerical",
                "min_value": 0.1,
                "max_value": 25.6,
                "average_value": 4.2,
                "unit": "g/t Au equivalent"
            },
            {
                "name": "tonnage",
                "type": "numerical",
                "min_value": 1000.0,
                "max_value": 50000.0,
                "average_value": 12500.0,
                "unit": "tonnes"
            }
        ],
        "collections": {
            "points": 89,
            "area_coverage": 225.0  # km²
        }
    },
    "exploration_drillholes_main": {
        "id": "obj_005",
        "name": "exploration_drillholes_main",
        "object_type": "downhole-collection",
        "description": "Main exploration drilling program results",
        "created_date": "2024-02-10T16:00:00Z",
        "created_by": "david.brown@seequent.com",
        "bounding_box": {
            "min_x": 342000.0,
            "max_x": 350000.0,
            "min_y": 6782000.0,
            "max_y": 6790000.0,
            "min_z": -800.0,
            "max_z": 100.0
        },
        "dimensions": {
            "length": 8000.0,  # max_x - min_x
            "width": 8000.0,   # max_y - min_y
            "depth": 900.0     # max_z - min_z
        },
        "assays": [
            {
                "element": "gold",
                "min_value": 0.002,
                "max_value": 35.7,
                "average_value": 4.8,
                "unit": "g/t"
            },
            {
                "element": "silver",
                "min_value": 0.1,
                "max_value": 278.9,
                "average_value": 32.1,
                "unit": "g/t"
            },
            {
                "element": "copper",
                "min_value": 0.005,
                "max_value": 5.6,
                "average_value": 1.4,
                "unit": "%"
            },
            {
                "element": "molybdenum",
                "min_value": 0.001,
                "max_value": 0.15,
                "average_value": 0.02,
                "unit": "%"
            },
            {
                "element": "uranium",
                "min_value": 0.5,
                "max_value": 125.0,
                "average_value": 15.8,
                "unit": "ppm"
            }
        ],
        "collections": {
            "holes": 78,
            "intervals": 2340,
            "total_length": 23400.0
        }
    },
    "structural_measurements_pointset": {
        "id": "obj_006",
        "name": "structural_measurements_pointset",
        "object_type": "pointset",
        "description": "Structural geology measurements and orientations",
        "created_date": "2024-02-15T13:30:00Z",
        "created_by": "emma.taylor@seequent.com",
        "bounding_box": {
            "min_x": 343000.0,
            "max_x": 348000.0,
            "min_y": 6783000.0,
            "max_y": 6788000.0,
            "min_z": -200.0,
            "max_z": 300.0
        },
        "dimensions": {
            "length": 5000.0,  # max_x - min_x
            "width": 5000.0,   # max_y - min_y
            "depth": 500.0     # max_z - min_z
        },
        "attributes": [
            {
                "name": "dip",
                "type": "numerical",
                "min_value": 5.0,
                "max_value": 90.0,
                "average_value": 45.2,
                "unit": "degrees"
            },
            {
                "name": "strike",
                "type": "numerical",
                "min_value": 0.0,
                "max_value": 360.0,
                "average_value": 180.0,
                "unit": "degrees"
            },
            {
                "name": "structure_type",
                "type": "categorical",
                "values": ["Bedding", "Foliation", "Fracture", "Fault", "Vein"],
                "dominant_value": "Bedding"
            },
            {
                "name": "confidence",
                "type": "categorical",
                "values": ["Low", "Medium", "High"],
                "dominant_value": "High"
            }
        ],
        "collections": {
            "points": 256,
            "area_coverage": 25.0  # km²
        }
    }
}


# Fake detailed version information for get_object_versions_info
FAKE_OBJECT_VERSIONS_INFO: Dict[str, Dict[str, Any]] = {
    "thalanga_local_drillholes_dt": {
        "id": "obj_001",
        "name": "thalanga_local_drillholes_dt",
        "object_type": "downhole-collection",
        "total_versions": 2,
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-01-10T08:00:00Z",
                "created_by": "john.smith@seequent.com",
                "description": "Initial version",
                "file_size": 125456,
                "file_size_unit": "bytes",
                "changes": [
                    "Initial upload of drilling data",
                    "Basic assay results for gold and silver",
                    "Collar and survey information"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 85.2,
                    "accuracy": 92.1,
                    "consistency": 89.5
                }
            },
            {
                "version_id": "v2",
                "created_date": "2024-01-15T10:30:00Z",
                "created_by": "john.smith@seequent.com",
                "description": "Updated with additional assays",
                "file_size": 156789,
                "file_size_unit": "bytes",
                "changes": [
                    "Added copper and zinc assay results",
                    "Updated quality control flags",
                    "Enhanced metadata information"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 94.6,
                    "accuracy": 94.8,
                    "consistency": 92.3
                }
            }
        ]
    },
    "thalanga_local_drillholes_e_sm": {
        "id": "obj_002",
        "name": "thalanga_local_drillholes_e_sm",
        "object_type": "downhole-collection",
        "total_versions": 3,
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-01-18T12:00:00Z",
                "created_by": "jane.doe@seequent.com",
                "description": "Initial enhanced version",
                "file_size": 198432,
                "file_size_unit": "bytes",
                "changes": [
                    "Enhanced drilling data with detailed assays",
                    "Multi-element analysis results",
                    "Improved spatial accuracy"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 88.7,
                    "accuracy": 91.2,
                    "consistency": 87.9
                }
            },
            {
                "version_id": "v2",
                "created_date": "2024-01-20T14:45:00Z",
                "created_by": "jane.doe@seequent.com",
                "description": "Added lead and iron assays",
                "file_size": 234567,
                "file_size_unit": "bytes",
                "changes": [
                    "Added lead and iron assay results",
                    "Updated detection limits",
                    "Enhanced QA/QC procedures"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 91.5,
                    "accuracy": 93.7,
                    "consistency": 90.8
                }
            },
            {
                "version_id": "v3",
                "created_date": "2024-01-25T16:15:00Z",
                "created_by": "jane.doe@seequent.com",
                "description": "Quality control and validation updates",
                "file_size": 245123,
                "file_size_unit": "bytes",
                "changes": [
                    "Comprehensive quality control review",
                    "Updated validation criteria",
                    "Enhanced metadata standards"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 96.8,
                    "accuracy": 96.3,
                    "consistency": 94.7
                }
            }
        ]
    },
    "surface_geology_pointset": {
        "id": "obj_003",
        "name": "surface_geology_pointset",
        "object_type": "pointset",
        "total_versions": 1,
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-01-25T09:15:00Z",
                "created_by": "mike.johnson@seequent.com",
                "description": "Initial surface geology data",
                "file_size": 67890,
                "file_size_unit": "bytes",
                "changes": [
                    "Initial surface geology sampling points",
                    "Rock type and formation classifications",
                    "Alteration intensity mapping"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 89.3,
                    "accuracy": 88.6,
                    "consistency": 91.2
                }
            }
        ]
    },
    "mineral_occurrences_pointset": {
        "id": "obj_004",
        "name": "mineral_occurrences_pointset",
        "object_type": "pointset",
        "total_versions": 2,
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-02-01T11:20:00Z",
                "created_by": "sarah.wilson@seequent.com",
                "description": "Initial mineral occurrences",
                "file_size": 45678,
                "file_size_unit": "bytes",
                "changes": [
                    "Initial mineral occurrence locations",
                    "Basic grade and mineral type information",
                    "Preliminary resource estimates"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 83.4,
                    "accuracy": 87.9,
                    "consistency": 85.6
                }
            },
            {
                "version_id": "v2",
                "created_date": "2024-02-05T15:30:00Z",
                "created_by": "sarah.wilson@seequent.com",
                "description": "Added tonnage estimates",
                "file_size": 52341,
                "file_size_unit": "bytes",
                "changes": [
                    "Added detailed tonnage estimates",
                    "Enhanced resource calculations",
                    "Improved confidence classifications"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 92.1,
                    "accuracy": 91.8,
                    "consistency": 89.4
                }
            }
        ]
    },
    "exploration_drillholes_main": {
        "id": "obj_005",
        "name": "exploration_drillholes_main",
        "object_type": "downhole-collection",
        "total_versions": 1,
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-02-10T16:00:00Z",
                "created_by": "david.brown@seequent.com",
                "description": "Main exploration drilling program results",
                "file_size": 312456,
                "file_size_unit": "bytes",
                "changes": [
                    "Comprehensive exploration drilling dataset",
                    "Multi-element assay results",
                    "Advanced geochemical analysis"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 97.2,
                    "accuracy": 95.6,
                    "consistency": 96.8
                }
            }
        ]
    },
    "structural_measurements_pointset": {
        "id": "obj_006",
        "name": "structural_measurements_pointset",
        "object_type": "pointset",
        "total_versions": 1,
        "versions": [
            {
                "version_id": "v1",
                "created_date": "2024-02-15T13:30:00Z",
                "created_by": "emma.taylor@seequent.com",
                "description": "Structural geology measurements and orientations",
                "file_size": 78234,
                "file_size_unit": "bytes",
                "changes": [
                    "Structural geology measurements",
                    "Dip and strike orientations",
                    "Structural confidence ratings"
                ],
                "validation_status": "passed",
                "data_quality": {
                    "completeness": 93.7,
                    "accuracy": 90.4,
                    "consistency": 88.9
                }
            }
        ]
    }
} 

# Fake table data for collections attributes
# Data is organized by object_name and collections_attribute
FAKE_TABLE_DATA: Dict[str, Dict[str, List[float]]] = {
    "thalanga_local_drillholes_dt": {
        "gold": [
            0.125, 0.087, 0.156, 0.092, 0.203, 0.078, 0.145, 0.112, 0.089, 0.167,
            0.134, 0.098, 0.176, 0.143, 0.087, 0.198, 0.156, 0.089, 0.123, 0.178,
            0.145, 0.092, 0.234, 0.156, 0.089, 0.167, 0.134, 0.098, 0.187, 0.123,
            0.156, 0.089, 0.145, 0.198, 0.123, 0.087, 0.167, 0.134, 0.156, 0.089,
            0.203, 0.145, 0.098, 0.187, 0.156, 0.123, 0.089, 0.167, 0.145, 0.134
        ],
        "silver": [
            12.5, 8.7, 15.6, 9.2, 20.3, 7.8, 14.5, 11.2, 8.9, 16.7,
            13.4, 9.8, 17.6, 14.3, 8.7, 19.8, 15.6, 8.9, 12.3, 17.8,
            14.5, 9.2, 23.4, 15.6, 8.9, 16.7, 13.4, 9.8, 18.7, 12.3,
            15.6, 8.9, 14.5, 19.8, 12.3, 8.7, 16.7, 13.4, 15.6, 8.9,
            20.3, 14.5, 9.8, 18.7, 15.6, 12.3, 8.9, 16.7, 14.5, 13.4
        ],
        "copper": [
            1.25, 0.87, 1.56, 0.92, 2.03, 0.78, 1.45, 1.12, 0.89, 1.67,
            1.34, 0.98, 1.76, 1.43, 0.87, 1.98, 1.56, 0.89, 1.23, 1.78,
            1.45, 0.92, 2.34, 1.56, 0.89, 1.67, 1.34, 0.98, 1.87, 1.23,
            1.56, 0.89, 1.45, 1.98, 1.23, 0.87, 1.67, 1.34, 1.56, 0.89,
            2.03, 1.45, 0.98, 1.87, 1.56, 1.23, 0.89, 1.67, 1.45, 1.34
        ],
        "zinc": [
            5.25, 3.87, 6.56, 4.92, 7.03, 3.78, 5.45, 4.12, 3.89, 6.67,
            5.34, 4.98, 6.76, 5.43, 3.87, 7.98, 5.56, 3.89, 4.23, 6.78,
            5.45, 4.92, 8.34, 5.56, 3.89, 6.67, 5.34, 4.98, 7.87, 4.23,
            5.56, 3.89, 5.45, 7.98, 4.23, 3.87, 6.67, 5.34, 5.56, 3.89,
            7.03, 5.45, 4.98, 7.87, 5.56, 4.23, 3.89, 6.67, 5.45, 5.34
        ]
    },
    "thalanga_local_drillholes_e_sm": {
        "gold": [
            0.342, 0.156, 0.287, 0.198, 0.423, 0.134, 0.276, 0.189, 0.156, 0.298,
            0.234, 0.167, 0.312, 0.245, 0.156, 0.387, 0.276, 0.189, 0.223, 0.356,
            0.267, 0.198, 0.434, 0.276, 0.189, 0.298, 0.234, 0.167, 0.367, 0.223,
            0.276, 0.189, 0.267, 0.387, 0.223, 0.156, 0.298, 0.234, 0.276, 0.189,
            0.423, 0.267, 0.167, 0.367, 0.276, 0.223, 0.189, 0.298, 0.267, 0.234
        ],
        "silver": [
            24.2, 15.6, 28.7, 19.8, 42.3, 13.4, 27.6, 18.9, 15.6, 29.8,
            23.4, 16.7, 31.2, 24.5, 15.6, 38.7, 27.6, 18.9, 22.3, 35.6,
            26.7, 19.8, 43.4, 27.6, 18.9, 29.8, 23.4, 16.7, 36.7, 22.3,
            27.6, 18.9, 26.7, 38.7, 22.3, 15.6, 29.8, 23.4, 27.6, 18.9,
            42.3, 26.7, 16.7, 36.7, 27.6, 22.3, 18.9, 29.8, 26.7, 23.4
        ],
        "copper": [
            2.42, 1.56, 2.87, 1.98, 4.23, 1.34, 2.76, 1.89, 1.56, 2.98,
            2.34, 1.67, 3.12, 2.45, 1.56, 3.87, 2.76, 1.89, 2.23, 3.56,
            2.67, 1.98, 4.34, 2.76, 1.89, 2.98, 2.34, 1.67, 3.67, 2.23,
            2.76, 1.89, 2.67, 3.87, 2.23, 1.56, 2.98, 2.34, 2.76, 1.89,
            4.23, 2.67, 1.67, 3.67, 2.76, 2.23, 1.89, 2.98, 2.67, 2.34
        ],
        "lead": [
            8.42, 5.56, 8.87, 6.98, 12.23, 4.34, 8.76, 6.89, 5.56, 9.98,
            8.34, 6.67, 10.12, 8.45, 5.56, 11.87, 8.76, 6.89, 7.23, 10.56,
            8.67, 6.98, 13.34, 8.76, 6.89, 9.98, 8.34, 6.67, 11.67, 7.23,
            8.76, 6.89, 8.67, 11.87, 7.23, 5.56, 9.98, 8.34, 8.76, 6.89,
            12.23, 8.67, 6.67, 11.67, 8.76, 7.23, 6.89, 9.98, 8.67, 8.34
        ],
        "zinc": [
            12.42, 8.56, 12.87, 9.98, 16.23, 7.34, 12.76, 9.89, 8.56, 13.98,
            12.34, 9.67, 14.12, 12.45, 8.56, 15.87, 12.76, 9.89, 11.23, 14.56,
            12.67, 9.98, 17.34, 12.76, 9.89, 13.98, 12.34, 9.67, 15.67, 11.23,
            12.76, 9.89, 12.67, 15.87, 11.23, 8.56, 13.98, 12.34, 12.76, 9.89,
            16.23, 12.67, 9.67, 15.67, 12.76, 11.23, 9.89, 13.98, 12.67, 12.34
        ],
        "iron": [
            45.2, 38.6, 47.8, 41.2, 52.3, 35.4, 46.7, 39.8, 38.6, 48.9,
            45.3, 40.7, 49.1, 45.8, 38.6, 51.2, 46.7, 39.8, 43.2, 49.6,
            46.2, 41.2, 54.3, 46.7, 39.8, 48.9, 45.3, 40.7, 50.7, 43.2,
            46.7, 39.8, 46.2, 51.2, 43.2, 38.6, 48.9, 45.3, 46.7, 39.8,
            52.3, 46.2, 40.7, 50.7, 46.7, 43.2, 39.8, 48.9, 46.2, 45.3
        ]
    },
    "exploration_drillholes_main": {
        "gold": [
            0.567, 0.234, 0.498, 0.312, 0.678, 0.189, 0.445, 0.298, 0.234, 0.512,
            0.389, 0.278, 0.534, 0.423, 0.234, 0.598, 0.445, 0.298, 0.367, 0.556,
            0.434, 0.312, 0.687, 0.445, 0.298, 0.512, 0.389, 0.278, 0.587, 0.367,
            0.445, 0.298, 0.434, 0.598, 0.367, 0.234, 0.512, 0.389, 0.445, 0.298,
            0.678, 0.434, 0.278, 0.587, 0.445, 0.367, 0.298, 0.512, 0.434, 0.389
        ],
        "silver": [
            34.7, 23.4, 49.8, 31.2, 67.8, 18.9, 44.5, 29.8, 23.4, 51.2,
            38.9, 27.8, 53.4, 42.3, 23.4, 59.8, 44.5, 29.8, 36.7, 55.6,
            43.4, 31.2, 68.7, 44.5, 29.8, 51.2, 38.9, 27.8, 58.7, 36.7,
            44.5, 29.8, 43.4, 59.8, 36.7, 23.4, 51.2, 38.9, 44.5, 29.8,
            67.8, 43.4, 27.8, 58.7, 44.5, 36.7, 29.8, 51.2, 43.4, 38.9
        ],
        "copper": [
            3.67, 2.34, 4.98, 3.12, 6.78, 1.89, 4.45, 2.98, 2.34, 5.12,
            3.89, 2.78, 5.34, 4.23, 2.34, 5.98, 4.45, 2.98, 3.67, 5.56,
            4.34, 3.12, 6.87, 4.45, 2.98, 5.12, 3.89, 2.78, 5.87, 3.67,
            4.45, 2.98, 4.34, 5.98, 3.67, 2.34, 5.12, 3.89, 4.45, 2.98,
            6.78, 4.34, 2.78, 5.87, 4.45, 3.67, 2.98, 5.12, 4.34, 3.89
        ],
        "molybdenum": [
            0.123, 0.089, 0.156, 0.098, 0.187, 0.067, 0.134, 0.112, 0.089, 0.145,
            0.121, 0.095, 0.167, 0.134, 0.089, 0.178, 0.134, 0.112, 0.123, 0.156,
            0.145, 0.098, 0.198, 0.134, 0.112, 0.145, 0.121, 0.095, 0.167, 0.123,
            0.134, 0.112, 0.145, 0.178, 0.123, 0.089, 0.145, 0.121, 0.134, 0.112,
            0.187, 0.145, 0.095, 0.167, 0.134, 0.123, 0.112, 0.145, 0.145, 0.121
        ],
        "uranium": [
            0.0045, 0.0023, 0.0067, 0.0034, 0.0089, 0.0019, 0.0056, 0.0041, 0.0023, 0.0072,
            0.0051, 0.0038, 0.0078, 0.0063, 0.0023, 0.0084, 0.0056, 0.0041, 0.0049, 0.0076,
            0.0058, 0.0034, 0.0095, 0.0056, 0.0041, 0.0072, 0.0051, 0.0038, 0.0081, 0.0049,
            0.0056, 0.0041, 0.0058, 0.0084, 0.0049, 0.0023, 0.0072, 0.0051, 0.0056, 0.0041,
            0.0089, 0.0058, 0.0038, 0.0081, 0.0056, 0.0049, 0.0041, 0.0072, 0.0058, 0.0051
        ]
    },
    "surface_geology_pointset": {
        "formation": [
            1.0, 2.0, 1.0, 3.0, 2.0, 1.0, 3.0, 2.0, 1.0, 2.0,
            3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 1.0,
            3.0, 2.0, 1.0, 3.0, 2.0, 1.0, 3.0, 2.0, 1.0, 2.0,
            1.0, 3.0, 2.0, 1.0, 3.0, 2.0, 1.0, 3.0, 2.0, 1.0,
            2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0
        ],
        "rock_type": [
            1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0, 4.0, 1.0, 2.0,
            3.0, 4.0, 1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0, 4.0,
            1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0, 4.0, 1.0, 2.0,
            3.0, 4.0, 1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0, 4.0,
            1.0, 2.0, 3.0, 4.0, 1.0, 2.0, 3.0, 4.0, 1.0, 2.0
        ],
        "alteration": [
            0.15, 0.23, 0.08, 0.45, 0.32, 0.17, 0.29, 0.12, 0.38, 0.26,
            0.19, 0.41, 0.07, 0.34, 0.28, 0.13, 0.47, 0.21, 0.35, 0.09,
            0.42, 0.18, 0.31, 0.25, 0.06, 0.39, 0.16, 0.44, 0.22, 0.33,
            0.11, 0.48, 0.24, 0.37, 0.14, 0.30, 0.05, 0.43, 0.20, 0.36,
            0.27, 0.10, 0.46, 0.19, 0.40, 0.15, 0.32, 0.08, 0.41, 0.23
        ]
    },
    "mineral_occurrences_pointset": {
        "mineral_type": [
            1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0,
            2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0,
            3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0,
            1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0,
            2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0
        ],
        "grade": [
            2.45, 1.67, 3.89, 2.12, 4.23, 1.34, 2.78, 1.89, 3.45, 2.67,
            1.98, 4.12, 1.56, 3.34, 2.89, 1.78, 4.45, 2.23, 3.67, 1.45,
            4.78, 2.01, 3.12, 2.56, 1.89, 4.34, 1.67, 3.78, 2.34, 3.89,
            1.23, 4.56, 2.78, 3.45, 1.90, 2.67, 1.12, 4.23, 2.45, 3.56,
            2.89, 1.34, 4.67, 2.12, 3.78, 1.56, 2.98, 1.78, 4.12, 2.34
        ],
        "tonnage": [
            125.4, 87.6, 189.3, 112.8, 203.5, 76.2, 145.7, 98.4, 167.9, 134.2,
            156.8, 201.3, 89.7, 178.5, 145.2, 92.1, 234.6, 123.8, 189.4, 87.3,
            212.7, 98.5, 167.2, 134.9, 78.6, 198.3, 112.4, 203.8, 145.7, 189.2,
            93.5, 234.1, 156.8, 178.3, 101.2, 167.9, 76.8, 201.5, 134.6, 189.7,
            145.3, 89.4, 223.8, 112.7, 198.5, 87.9, 167.4, 98.2, 201.3, 134.8
        ]
    },
    "structural_measurements_pointset": {
        "dip": [
            35.2, 42.8, 28.7, 51.3, 39.6, 33.9, 47.2, 31.5, 44.8, 38.1,
            29.6, 48.7, 35.4, 41.2, 33.8, 46.9, 30.7, 43.5, 37.2, 32.1,
            49.8, 36.3, 40.7, 34.5, 45.1, 31.9, 42.6, 38.8, 33.4, 47.3,
            35.7, 41.9, 29.2, 44.6, 37.5, 32.8, 48.1, 34.2, 43.7, 39.4,
            31.6, 46.8, 35.9, 40.3, 33.7, 45.5, 30.1, 42.9, 38.6, 34.8
        ],
        "strike": [
            125.4, 087.6, 189.3, 112.8, 203.5, 076.2, 145.7, 098.4, 167.9, 134.2,
            156.8, 201.3, 089.7, 178.5, 145.2, 092.1, 234.6, 123.8, 189.4, 087.3,
            212.7, 098.5, 167.2, 134.9, 078.6, 198.3, 112.4, 203.8, 145.7, 189.2,
            093.5, 234.1, 156.8, 178.3, 101.2, 167.9, 076.8, 201.5, 134.6, 189.7,
            145.3, 089.4, 223.8, 112.7, 198.5, 087.9, 167.4, 098.2, 201.3, 134.8
        ],
        "structure_type": [
            1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0,
            2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0,
            3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0,
            1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0,
            2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0, 3.0, 1.0, 2.0
        ],
        "confidence": [
            0.85, 0.92, 0.78, 0.89, 0.93, 0.81, 0.88, 0.76, 0.91, 0.87,
            0.82, 0.94, 0.79, 0.86, 0.90, 0.83, 0.95, 0.77, 0.89, 0.84,
            0.96, 0.80, 0.87, 0.91, 0.75, 0.93, 0.85, 0.88, 0.82, 0.90,
            0.78, 0.94, 0.86, 0.89, 0.81, 0.92, 0.76, 0.95, 0.87, 0.83,
            0.89, 0.79, 0.93, 0.85, 0.88, 0.82, 0.91, 0.77, 0.94, 0.86
        ]
    }
} 