import re
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any, Optional

class WeatherDataParser:
    """
    Parser for fixed-width meteorological data format
    Handles WNDRAD (Wind Radar) data and similar weather station formats
    """
    
    def __init__(self):
        self.header_info = {}
        self.measurements = []
        self.missing_data_markers = ['//////', '///////', '/////']
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse the weather data file and return structured data
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return self.parse_content(content)
    
    def parse_content(self, content: str) -> Dict[str, Any]:
        """
        Parse weather data content from string
        """
        lines = content.strip().split('\n')
        
        # Parse header information
        self._parse_header(lines)
        
        # Parse measurement data
        self._parse_measurements(lines)
        
        return {
            'header': self.header_info,
            'measurements': self.measurements,
            'summary': self._generate_summary()
        }
    
    def _parse_header(self, lines: List[str]) -> None:
        """
        Extract header information from the first few lines
        """
        for i, line in enumerate(lines[:10]):  # Check first 10 lines for header info
            line = line.strip()
            
            # Parse instrument type and version
            if 'WNDRAD' in line:
                parts = line.split()
                if len(parts) >= 2:
                    self.header_info['instrument_type'] = parts[0]
                    self.header_info['version'] = parts[1]
            
            # Parse station ID and coordinates
            elif re.match(r'^\d{5}\s+\d+\.\d+\s+\d+\.\d+', line):
                parts = line.split()
                if len(parts) >= 3:
                    self.header_info['station_id'] = parts[0]
                    self.header_info['longitude'] = float(parts[1])
                    self.header_info['latitude'] = float(parts[2])
                    if len(parts) > 3:
                        self.header_info['elevation'] = float(parts[3])
            
            # Parse timestamp information
            elif re.search(r'\d{14}', line):  # 14-digit timestamp
                timestamps = re.findall(r'\d{14}', line)
                if timestamps:
                    self.header_info['start_time'] = self._parse_timestamp(timestamps[0])
                    if len(timestamps) > 1:
                        self.header_info['end_time'] = self._parse_timestamp(timestamps[1])
            
            # Parse measurement type indicator
            elif 'RAD FIRST' in line:
                self.header_info['measurement_type'] = 'RAD_FIRST'
                self.header_info['data_start_line'] = i + 1
                break
    
    def _parse_timestamp(self, timestamp_str: str) -> Optional[datetime]:
        """
        Parse 14-digit timestamp (YYYYMMDDHHMMSS)
        """
        try:
            return datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
        except ValueError:
            return None
    
    def _parse_measurements(self, lines: List[str]) -> None:
        """
        Parse measurement data from data lines
        """
        data_start = self.header_info.get('data_start_line', 0)
        
        for line_num, line in enumerate(lines[data_start:], start=data_start):
            line = line.strip()
            if not line or 'RAD FIRST' in line:
                continue
            
            # Parse altitude and measurement values
            measurement = self._parse_measurement_line(line, line_num)
            if measurement:
                self.measurements.append(measurement)
    
    def _parse_measurement_line(self, line: str, line_num: int) -> Optional[Dict[str, Any]]:
        """
        Parse individual measurement line
        """
        # Skip lines that are all missing data markers
        if all(marker in line for marker in self.missing_data_markers):
            return {
                'line_number': line_num,
                'altitude': self._extract_altitude(line),
                'status': 'missing_data',
                'values': []
            }
        
        # Extract numerical values
        values = []
        parts = line.split()
        
        altitude = None
        if parts:
            # First part is usually altitude in meters
            try:
                altitude = int(parts[0])
            except ValueError:
                pass
        
        # Extract measurement values
        for part in parts[1:]:
            if any(marker in part for marker in self.missing_data_markers):
                values.append(None)  # Missing data
            else:
                try:
                    # Try to parse as float
                    value = float(part)
                    values.append(value)
                except ValueError:
                    # Skip non-numeric values
                    pass
        
        return {
            'line_number': line_num,
            'altitude': altitude,
            'status': 'valid' if values else 'no_data',
            'values': values,
            'raw_line': line
        }
    
    def _extract_altitude(self, line: str) -> Optional[int]:
        """
        Extract altitude from measurement line
        """
        # Look for altitude pattern at the beginning
        match = re.match(r'^(\d{5})', line)
        if match:
            return int(match.group(1))
        return None
    
    def _generate_summary(self) -> Dict[str, Any]:
        """
        Generate summary statistics
        """
        valid_measurements = [m for m in self.measurements if m['status'] == 'valid']
        missing_measurements = [m for m in self.measurements if m['status'] == 'missing_data']
        
        return {
            'total_lines': len(self.measurements),
            'valid_measurements': len(valid_measurements),
            'missing_measurements': len(missing_measurements),
            'altitude_range': self._get_altitude_range(),
            'measurement_count_per_altitude': self._count_measurements_per_altitude()
        }
    
    def _get_altitude_range(self) -> Dict[str, Optional[int]]:
        """
        Get altitude range from measurements
        """
        altitudes = [m['altitude'] for m in self.measurements if m['altitude'] is not None]
        if altitudes:
            return {'min': min(altitudes), 'max': max(altitudes)}
        return {'min': None, 'max': None}
    
    def _count_measurements_per_altitude(self) -> Dict[int, int]:
        """
        Count valid measurements per altitude level
        """
        altitude_counts = {}
        for measurement in self.measurements:
            if measurement['altitude'] and measurement['status'] == 'valid':
                alt = measurement['altitude']
                altitude_counts[alt] = altitude_counts.get(alt, 0) + 1
        return altitude_counts
    
    def to_dataframe(self) -> pd.DataFrame:
        """
        Convert measurements to pandas DataFrame
        """
        data = []
        for measurement in self.measurements:
            row = {
                'line_number': measurement['line_number'],
                'altitude': measurement['altitude'],
                'status': measurement['status']
            }
            
            # Add measurement values as separate columns
            for i, value in enumerate(measurement.get('values', [])):
                row[f'measurement_{i+1}'] = value
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def print_summary(self) -> None:
        """
        Print formatted summary of parsed data
        """
        print("=== Weather Data Parser Summary ===\n")
        
        # Header information
        print("Header Information:")
        for key, value in self.header_info.items():
            print(f"  {key}: {value}")
        
        print(f"\nData Summary:")
        summary = self._generate_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")
        
        # Sample measurements
        print(f"\nSample Measurements (first 5):")
        for i, measurement in enumerate(self.measurements[:5]):
            print(f"  Line {measurement['line_number']}: Alt={measurement['altitude']}m, "
                  f"Status={measurement['status']}, Values={measurement.get('values', [])}")


# Example usage and test function
def test_parser_with_sample_data():
    """
    Test the parser with sample data similar to the image
    """
    sample_data = """print(content)

WNDRAD 01.20
58235 0118.8472 032.3686 00016.2 LC
32 03.0 15.0 15.0 15.0 15.0 00.0 00.0 5 060 0232 25000 00.4 04 04 02.0 00.0 00100 03100
0 20250801235400 20250802000000 3 016 064 0512 016 ELWSN/ 036.3 036.3 036.3 036.3
RAD FIRST
00100 0001.1 0016.8 0001.2
00160 0001.1 0025.5 0001.0
00220 0000.8 0009.4 0000.7
00280 0000.8 0005.8 0000.5
00340 0001.4 0016.8 0000.2
00400 0001.5 0024.7 -000.4
00460 ////// ////// //////
00520 ////// ////// //////
00580 ////// ////// //////
00640 ////// ////// //////
00700 ////// ////// //////
00760 ////// ////// //////
00820 ////// ////// //////"""

    # Create parser and parse the sample data
    parser = WeatherDataParser()
    result = parser.parse_content(sample_data)
    
    # Print results
    parser.print_summary()
    
    # Convert to DataFrame and show
    df = parser.to_dataframe()
    print(f"\nDataFrame Shape: {df.shape}")
    print(f"\nFirst 10 rows:")
    print(df.head(10))
    
    return parser, result, df

# Run the test
if __name__ == "__main__":
    parser, result, df = test_parser_with_sample_data()

    