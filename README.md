_Disclaimer: This content is intended to be treated as sample code. As the adage goes, you get what you pay for._

# OCI Network Discovery

OCI Network Discovery (oci-net-disco) is a small tool that searches for VNICs (Virtual Network Interface Card) in Oracle Cloud Infrastructure. The intention is to make it easier to locate and analyze what is connected to VCN (Virtual Cloud Network) subnets. This can be a requirement because termination of a deprecated network is failing due to a stray VNIC being connected, or simply for general awareness and good observability practice.

## Requirements

- Python 3.9 or greater
- _Recommended:_ A Virtual Environment to install packages
- OCI package given in requirements.txt
- An OCI account profile with permissions to read VNICs in the desired location

## Usage

```python disco.py [-c COMPARMENT_OCID][-s SUBNET_OCID][-p PROFILE][--ip|--dt]```

Get All VNICs:
```python disco.py```

Get All VNICs on subnet _foo_:
```python disco.py -s foo```

Get all VNICs in compartment _bar_:
```python disco.py -c bar```

Get all VNICs in compartment _bar_ on subnet _foo_:
```python disco.py -s foo -c bar```

### Inputs

All flags are optional:
- [-c/--compartment] Compartment OCID -- Scope search to a defined compartment in OCI
- [-s/--subnet] Subnet OCID -- Scope search to a defined subnet in OCI
- [--ip] Use Instance Principal Authentication (Requires Dynamic-Group)
- [--dt] Use Delegation Token Authentication (Requries Cloud Shell)
- [-p/--profile] OCI Config File _(~/.oci/config)_ Profile to use

### Outputs

The output of the script will be a JSON formatted list of VNICs. VNIC properties will be exposed in as much detail as possible, which may give an indication of what the VNIC is attached to and/or its location.
