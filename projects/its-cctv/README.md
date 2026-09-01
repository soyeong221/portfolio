# ITS CCTV Monitoring System

> C# WPF와 ASP.NET Core Web API를 활용한 실시간 CCTV 조회·모니터링 시스템

## 시스템 구현

<p align="center">
  <img src="./images/cctv-system.png" width="900" alt="ITS CCTV 모니터링 시스템"/>
</p>

국가교통정보센터 ITS Open API의 CCTV 데이터를 ASP.NET Core Web API를 통해 조회하고,
WPF Client에서 CCTV 정보·위치·실시간 영상을 하나의 화면에서 확인할 수 있도록 구현했습니다.

<br>

## 동작 결과

<table>
  <tr>
    <td align="center" width="33%">
      <img src="./images/cctv-list.png" width="100%" alt="CCTV 조회 결과"/>
      <br>
      <b>CCTV 조회</b>
      <br>
      지역 및 조건에 따른 CCTV 정보 조회
    </td>
    <td align="center" width="33%">
      <img src="./images/cctv-stream.png" width="100%" alt="CCTV 영상 재생"/>
      <br>
      <b>실시간 영상</b>
      <br>
      LibVLCSharp 기반 HLS CCTV 스트림 재생
    </td>
    <td align="center" width="33%">
      <img src="./images/cctv-map.png" width="100%" alt="CCTV 지도 연동"/>
      <br>
      <b>지도 연동</b>
      <br>
      CCTV 위치 및 상세정보 표시
    </td>
  </tr>
</table>

<br>

## 🔗 **Original Project**

> WPF Client와 ASP.NET Core Web API 연동부터 ITS Open API 데이터 조회, CCTV 영상 재생 및 지도 연동까지의 전체 구현 과정을 확인할 수 있습니다.

[View on GitHub](https://github.com/soyeong221/iot-dotnet-2026/blob/main/TOYPROJECT1.md)

---

## 프로젝트 개요

국가교통정보센터 ITS Open API에서 CCTV 정보를 조회하고,
실시간 영상과 위치 정보를 하나의 WPF 응용프로그램에서 확인할 수 있도록 구현한 프로젝트입니다.

WPF Client가 외부 Open API를 직접 호출하지 않고 ASP.NET Core Web API를 Bridge Server로 구성하여
외부 API 요청과 데이터 처리를 담당하도록 분리했습니다.

이를 통해 API 인증키를 Client에서 분리하고,
외부 데이터 조회와 사용자 화면 표시 기능의 역할을 구분했습니다.

## 프로젝트 정보

| 항목 | 내용 |
|---|---|
| 개발 형태 | 개인 토이 프로젝트 |
| 핵심 기술 | C#, WPF, ASP.NET Core Web API, LibVLCSharp, WebView2, Leaflet.js |
| 데이터 | 국가교통정보센터 ITS Open API |
| 핵심 기능 | CCTV 조회, HLS 영상 재생, 지도 연동, 상세정보 표시 |

## 주요 기능

- C# WPF 기반 CCTV 조회·모니터링 응용프로그램 구현
- ASP.NET Core Web API 기반 Bridge Server 구성
- 국가교통정보센터 ITS Open API CCTV 데이터 조회
- API 인증키를 Client에서 분리하여 Server에서 관리
- CCTV 데이터 JSON 직렬화·역직렬화
- LibVLCSharp 기반 HLS CCTV 스트림 재생
- WebView2를 활용한 웹 콘텐츠 연동
- Leaflet.js 기반 CCTV 위치 지도 표시
- CCTV 선택 시 영상·지도·상세정보 연동

## 시스템 흐름

```text
WPF Client
    ↓ HTTP / JSON
ASP.NET Core Web API
    (Bridge Server)
    ↓ HTTP / API Request
국가교통정보센터 ITS Open API
```

WPF Client에서 검색 조건을 Bridge Server로 전달하고,
ASP.NET Core Web API에서 외부 ITS Open API를 호출하여 CCTV 데이터를 조회하도록 구성했습니다.

조회된 데이터는 JSON 형태로 WPF Client에 전달되며,
선택한 CCTV의 위치·상세정보·HLS 영상을 하나의 화면에서 확인할 수 있도록 연동했습니다.

## 핵심 구현 코드

### 1. WPF Client에서 Bridge API 호출

WPF Client에서 검색 조건을 JSON으로 변환하여 ASP.NET Core Web API에 전달하고,
응답받은 CCTV 데이터를 다시 객체로 변환하여 화면에서 사용할 수 있도록 구성했습니다.

```csharp
var json = JsonSerializer.Serialize(searchCondition);
var content = new StringContent(
    json,
    Encoding.UTF8,
    "application/json"
);

var response = await client.PostAsync(apiUrl, content);

if (response.IsSuccessStatusCode)
{
    var result = await response.Content.ReadAsStringAsync();

    var cctvList =
        JsonSerializer.Deserialize<List<CctvInfo>>(result);

    return cctvList;
}
```

**구현 포인트**
- WPF Client에서 검색 조건을 JSON으로 직렬화
- `HttpClient`를 이용하여 Bridge API 호출
- Server 응답 데이터를 역직렬화하여 CCTV 객체로 변환
- Client가 외부 ITS API를 직접 호출하지 않는 구조로 분리

### 2. ASP.NET Core Web API에서 ITS Open API 호출

Bridge Server에서 Client의 요청을 받아 ITS Open API를 호출하고,
응답 데이터를 Client에서 사용할 수 있는 형태로 변환하여 반환했습니다.

```csharp
var apiKey = configuration["ItsApi:ApiKey"];

var url =
    $"{baseUrl}?apiKey={apiKey}" +
    $"&type={request.Type}" +
    $"&cctvType={request.CctvType}";

var response = await httpClient.GetAsync(url);
response.EnsureSuccessStatusCode();

var json =
    await response.Content.ReadAsStringAsync();

var result =
    JsonSerializer.Deserialize<ItsCctvResponse>(json);
```

**구현 포인트**
- API Key를 Server 설정에서 관리
- Client에서 받은 검색 조건을 ITS API 요청에 반영
- `HttpClient`를 활용한 외부 Open API 호출
- 외부 API 응답을 역직렬화하여 Client에 전달

### 3. CCTV 선택 시 영상·지도·상세정보 연동

사용자가 CCTV 목록에서 항목을 선택하면
해당 CCTV의 실시간 영상과 지도 위치, 상세정보가 함께 갱신되도록 구성했습니다.

```csharp
private void GrdCctv_SelectionChanged(
    object sender,
    SelectionChangedEventArgs e)
{
    if (GrdCctv.SelectedItem is CctvInfo selected)
    {
        PlayCctv(selected.CctvUrl);

        ShowMarker(
            selected.CoordY,
            selected.CoordX,
            selected.CctvName
        );

        SetDetailInfo(selected);
    }
}
```

**구현 포인트**
- CCTV 선택 이벤트를 기준으로 관련 기능 연동
- LibVLCSharp을 이용한 HLS 영상 재생
- WebView2·Leaflet.js를 이용한 CCTV 위치 표시
- 선택한 CCTV의 영상·지도·상세정보를 하나의 화면에서 제공

## 대표 트러블슈팅

### 1. API 인증키의 Client 노출

**문제**  
초기 구조에서는 WPF Client에서 ITS Open API를 직접 호출하여
API 인증키가 Client 코드에 포함되는 문제가 있었습니다.

**해결**  
ASP.NET Core Web API를 Bridge Server로 추가하고,
API 인증키와 외부 API 호출을 Server에서 관리하도록 구조를 변경했습니다.

### 2. Client와 Server 간 데이터 모델 불일치

**문제**  
WPF Client와 ASP.NET Core Server에서 사용하는 데이터 모델의
속성명과 구조가 일치하지 않아 JSON 역직렬화 과정에서 데이터가 정상적으로 전달되지 않는 문제가 발생했습니다.

**해결**  
Client와 Server의 DTO 구조 및 JSON 속성을 비교하여 데이터 형식을 일치시키고,
요청·응답 데이터가 정상적으로 변환되도록 수정했습니다.

### 3. Client와 Server 간 포트 불일치

**문제**  
ASP.NET Core 서버의 실행 프로필에 따라 포트가 달라지면서
WPF Client에서 Bridge API 호출 시 연결이 거부되는 문제가 발생했습니다.

**해결**  
ASP.NET Core 실행 로그의 `Now listening on` 주소와
WPF Client에 설정된 Bridge API 주소를 비교하여 포트를 일치시키고 통신을 정상화했습니다.

## 프로젝트 결과

- C# WPF 기반 CCTV 조회·모니터링 응용프로그램 구현
- WPF Client와 ASP.NET Core Web API 간 데이터 연동
- Bridge Server를 통한 ITS Open API 데이터 조회 구조 구현
- LibVLCSharp을 활용한 HLS CCTV 실시간 영상 재생
- WebView2·Leaflet.js 기반 CCTV 위치 지도 연동
- 데이터 조회, 영상 재생, 지도 및 상세정보 표시 기능을 하나의 WPF 응용프로그램으로 통합

> 이 포트폴리오 폴더는 프로젝트를 설명하기 위한 요약본입니다. 실제 소스코드와 상세 개발 과정은 원본 GitHub 저장소에서 관리합니다.
