# ITS CCTV Monitoring System

> ITS OpenAPI 기반 실시간 CCTV 영상·지도 통합 모니터링 시스템

## 실행 화면

<p align="center">
  <img width="1237" height="692" alt="ITS CCTV Monitoring System 실행 화면" src="https://github.com/user-attachments/assets/7abce5ea-9555-40fe-9ab4-8c861c2b8feb" />
</p>

<br>

## 실행 영상

https://github.com/user-attachments/assets/4ca559a0-485a-4708-af60-494a696dbcf1

<br>

## 🔗 **Original Project**

[View on GitHub](https://github.com/soyeong221/iot-dotnet-2026/blob/main/TOYPROJECT1.md#국가교통정보센터-cctv-모니터링-시스템)

---

## 프로젝트 개요

국가교통정보센터 ITS Open API를 활용하여 전국 고속도로·국도 CCTV를 검색하고,
실시간 영상과 위치 정보를 함께 확인할 수 있도록 구현한 WPF 기반 데스크톱 애플리케이션입니다.

WPF 클라이언트가 외부 Open API를 직접 호출하지 않고,
ASP.NET Core Web API로 구현한 Bridge Server를 통해 데이터를 전달받도록 구성했습니다.

이를 통해 API 인증키를 클라이언트에서 분리하고,
외부 API 요청과 화면 표시 기능의 역할을 구분했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 프로젝트 유형 | 개인 토이 프로젝트 |
| Client | C#, WPF, Wpf.Ui, WebView2, LibVLCSharp |
| Server | ASP.NET Core Web API |
| Map | Leaflet.js |
| Data | 국가교통정보센터 ITS Open API |
| 주요 기능 | CCTV 검색, 실시간 영상 재생, 지도 표시, 상세정보 조회 |

## 주요 기능

<p align="left">
  <img src="https://github.com/user-attachments/assets/80429187-bc10-4f9d-beac-4c54fcae1f64" width="1000" alt="ITS CCTV 기본 화면"/>
</p>

- 전국 시·도 단위의 위도·경도 범위를 이용한 CCTV 검색
- 고속도로와 국도 CCTV 구분 조회
- 검색 중 ProgressBar를 이용한 진행 상태 표시
- 초기화 버튼을 통한 검색 조건, 목록, 영상 및 지도 초기화

<br>

<p align="left">
  <img src="https://github.com/user-attachments/assets/ed683467-1581-406e-b848-3ecdbaa022f7" width="1000" alt="ITS CCTV 정상 실행 화면"/>
</p>

- LibVLCSharp을 활용한 HLS 실시간 영상 재생
- WebView2와 Leaflet.js를 활용한 CCTV 위치 지도 표시
- 선택한 CCTV의 이름, 좌표, 영상 URL 등 상세정보 제공
- WPF 클라이언트와 ASP.NET Core Web API 연동

<br>

<p align="left">
  <img src="https://github.com/user-attachments/assets/4bc9016a-a79a-49c4-bb1c-511f9954893f" width="1000" alt="ITS CCTV 스트리밍 연결 불량 화면"/>
</p>

- 스트리밍 연결 성공·실패 상태 표시
- 영상 재생 실패 및 API 키 누락 등에 대한 예외 처리

## 시스템 흐름

```text
WPF Client
       │
       │ HTTP / JSON
       ↓
ASP.NET Core Web API
    (Bridge Server)
       │
       │ HTTP / API Request
       ↓
국가교통정보센터 ITS Open API
       │
       │ CCTV Data
       ↓
ASP.NET Core Web API
       │
       │ HTTP / JSON
       ↓
WPF Client
       ├─ CCTV List
       ├─ LibVLCSharp HLS Player
       ├─ WebView2 + Leaflet Map
       └─ CCTV Detail
```

## 핵심 구현 코드

### 1. WPF Client → Bridge API 연동

WPF 클라이언트에서 검색 조건을 Bridge API로 전달하고,
응답받은 JSON 데이터를 CCTV 목록으로 변환하도록 구성했습니다.

```csharp
public async Task<List<CctvResultDto>> GetBridgeApiAsync(CctvRequest request)
{
    var req = new HttpRequestMessage(HttpMethod.Get, AppCommon.baseUrl);

    req.Content = new StringContent(
        JsonConvert.SerializeObject(request),
        Encoding.UTF8,
        "application/json");

    var response = await httpClient.SendAsync(req);
    string json = await response.Content.ReadAsStringAsync();

    var result = JsonConvert.DeserializeObject<List<CctvResultDto>>(json);

    if (result == null) return new();
    else return result;
}
```

**구현 포인트**

- WPF Client와 외부 ITS API 호출 역할 분리
- 검색 조건을 JSON으로 직렬화하여 Bridge API에 전달
- 응답 JSON을 `CctvResultDto` 목록으로 역직렬화
- 클라이언트에서는 화면 처리에 필요한 데이터만 사용

### 2. Bridge Server → ITS Open API 호출

Bridge Server에서 설정 파일의 API 인증키를 읽고,
검색 조건을 ITS Open API 요청 파라미터로 구성했습니다.

응답 데이터는 화면에서 사용할 필드만 `CctvResultDto`로 변환하여
WPF 클라이언트에 전달하도록 구성했습니다.

```csharp
public async Task<List<CctvResultDto>> GetCctvSearchAsync(CctvRequest request)
{
    var apiKey = configuration["ItsOpenApi:ApiKey"];

    var url = $"?apiKey={apiKey}" +
              $"&type={request.RoadType}" +
              $"&cctvType={request.CctvType}" +
              $"&minX={request.MinX}" +
              $"&maxX={request.MaxX}" +
              $"&minY={request.MinY}" +
              $"&maxY={request.MaxY}" +
              $"&getType={request.GetRetType}";

    string json = await httpClient.GetStringAsync(url);

    var result = JsonConvert.DeserializeObject<CctvResponse>(json);

    if (result == null)
        return new();

    return result.Response.Data.Select(x => new CctvResultDto
    {
        CctvName = x.CctvName,
        CoordX = Convert.ToDouble(x.CoordX),
        CoordY = Convert.ToDouble(x.CoordY),
        CctvType = Convert.ToInt32(x.CctvType),
        CctvFormat = x.CctvFormat,
        CctvUrl = x.CctvUrl,
    }).ToList();
}
```

**구현 포인트**

- API 인증키를 WPF Client가 아닌 Server 설정에서 관리
- 검색 조건을 외부 API 요청 파라미터로 변환
- ITS Open API 응답 JSON 역직렬화
- 필요한 데이터만 DTO로 변환하여 Client에 전달

### 3. CCTV 선택 시 영상·지도·상세정보 연동

목록에서 CCTV를 선택하면 동일한 CCTV 정보를 기준으로
실시간 영상, 지도 위치, 상세정보를 함께 갱신하도록 구성했습니다.

```csharp
private async void LsbCctv_SelectionChanged(
    object sender,
    SelectionChangedEventArgs e)
{
    if (LsbCctv.SelectedItem is not CctvResultDto selected)
        return;

    PlayCctv(selected.CctvUrl);
    await ShowMarkerAsync(selected);

    SetDetailInfo(selected);
    DisplayStatusBarInfo(selected);
}
```

실시간 CCTV 영상은 LibVLCSharp을 이용하여 HLS URL을 재생합니다.

```csharp
private async Task PlayCctv(string url)
{
    if (string.IsNullOrWhiteSpace(url))
        return;

    try
    {
        mediaPlayer.Stop();

        using var media = new Media(libVLC, new Uri(url));
        mediaPlayer.Play(media);
    }
    catch (Exception ex)
    {
        await ShowMessageAsync(
            "오류",
            $"스트리밍 재생 오류 발생 : {ex.Message}");
    }
}
```

지도는 WebView2에서 Leaflet JavaScript 함수를 실행하여
선택한 CCTV 좌표로 마커를 이동합니다.

```csharp
string script = $"moveMarker({lat}, {lng}, '{name}');";
await WvwMap.ExecuteScriptAsync(script);
```

**구현 포인트**

- CCTV 선택 이벤트를 기준으로 영상·지도·상세정보 동기화
- LibVLCSharp을 이용한 HLS 실시간 영상 재생
- WebView2에서 Leaflet JavaScript 함수 실행
- 하나의 CCTV 데이터를 여러 UI 영역에 연동

## 대표 트러블슈팅

### 1. API 인증키 클라이언트 노출

**문제**  
초기에는 WPF 클라이언트에서 ITS Open API를 직접 호출하여
API 인증키가 클라이언트 코드에 포함되는 구조였습니다.

**해결**  
ASP.NET Core Web API를 Bridge Server로 추가하고,
API 인증키와 외부 API 호출 로직을 서버로 분리했습니다.

### 2. Client / Server 데이터 모델 불일치

**문제**  
Bridge API의 응답 구조와 WPF 클라이언트에서 사용하는 모델이 일치하지 않아
역직렬화 및 화면 표시 과정에서 데이터 처리 문제가 발생했습니다.

**해결**  
`CctvResultDto`를 기준으로 필요한 필드와 데이터 타입을 맞추어
Client와 Server 간 데이터 구조를 통일했습니다.

### 3. Client / Server 포트 불일치

**문제**  
ASP.NET Core 서버의 실행 프로필에 따라 포트가 달라지면서
WPF 클라이언트에서 Bridge API 호출 시 연결이 거부되는 문제가 발생했습니다.

**해결**  
ASP.NET Core 실행 로그의 `Now listening on` 주소와
WPF 클라이언트에 설정된 Bridge API 주소를 비교하여 포트를 일치시키고 통신을 정상화했습니다.

## 프로젝트 결과

- ITS Open API 기반 전국 CCTV 검색 기능 구현
- ASP.NET Core Web API를 통한 외부 API 요청 및 인증키 분리
- LibVLCSharp 기반 HLS 실시간 CCTV 영상 재생
- WebView2 + Leaflet.js 기반 CCTV 위치 지도 연동
- CCTV 선택 시 영상·지도·상세정보 동기화
- **WPF Client → Bridge API → ITS Open API**로 역할을 분리한 시스템 구조 구현

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드와 상세 개발 과정은 원본 GitHub 저장소에서 관리합니다.
