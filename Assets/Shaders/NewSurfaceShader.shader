Shader "Custom/BlackExceptOne" {
    Properties {
        _MainTex ("Texture", 2D) = "white" {}
    }
    SubShader {
        Tags { "RenderType"="Opaque" }
        LOD 200
        
        CGPROGRAM
        #pragma surface surf Standard fullforwardshadows

        struct Input {
            float2 uv_MainTex;
        };

        sampler2D _MainTex;

        void surf (Input IN, inout SurfaceOutputStandard o) {
            o.Albedo = float3(0,0,0); // Set color to black
        }
        ENDCG
    }
    FallBack "Diffuse"
}